use pyo3::prelude::*;
use pyo3::exceptions::PyIOError;
use rayon::prelude::*;
use std::fs::File;
use std::io::{BufRead, BufReader, Read};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};
use zip::ZipArchive;

#[pyclass]
pub struct BruteForce {
    actual_trys: Arc<AtomicU64>,
    found: Arc<AtomicBool>,
    result: Arc<parking_lot::Mutex<Option<String>>>,
}

#[pymethods]
impl BruteForce {
    #[new]
    #[pyo3(signature = (src=None))]
    fn new(src: Option<String>) -> Self {
        let _ = src;
        BruteForce {
            actual_trys: Arc::new(AtomicU64::new(0)),
            found: Arc::new(AtomicBool::new(false)),
            result: Arc::new(parking_lot::Mutex::new(None)),
        }
    }

    fn get_tries(&self) -> u64 {
        self.actual_trys.load(Ordering::Relaxed)
    }

    fn is_found(&self) -> bool {
        self.found.load(Ordering::Relaxed)
    }

    fn get_result(&self) -> Option<String> {
        self.result.lock().clone()
    }

    fn reset(&self) {
        self.actual_trys.store(0, Ordering::Relaxed);
        self.found.store(false, Ordering::Relaxed);
        *self.result.lock() = None;
    }

    #[pyo3(signature = (zip_path, wordlist_path, callback=None, batch_size=None))]
    fn crack(
        &self,
        py: Python,
        zip_path: String,
        wordlist_path: String,
        callback: Option<PyObject>,
        batch_size: Option<usize>,
    ) -> PyResult<Option<String>> {
        self.reset();
        
        let batch_size = batch_size.unwrap_or(50000);
        
        let actual_trys = self.actual_trys.clone();
        let found = self.found.clone();
        let result = self.result.clone();
        
        let final_result = py.allow_threads(|| {
            let file = File::open(&wordlist_path)
                .map_err(|e| format!("Error opening wordlist: {}", e))?;
            
            let reader = BufReader::with_capacity(128 * 1024, file);
            let mut passwords = Vec::with_capacity(batch_size);
            
            let mut batches_processed = 0u64;
            let start_time = Instant::now();
            let mut last_callback_time = Instant::now();

            for line in reader.lines() {
                if found.load(Ordering::Relaxed) {
                    break;
                }

                let password = line.map_err(|e| format!("Error reading line: {}", e))?;
                passwords.push(password);

                if passwords.len() >= batch_size {
                    let result_found = Self::process_batch_static(
                        &zip_path,
                        &passwords,
                        &actual_trys,
                        &found,
                        &result,
                    )?;

                    batches_processed += 1;

                    if result_found.is_some() {
                        return Ok(result_found);
                    }

                    passwords.clear();

                    if batches_processed % 5 == 0 && last_callback_time.elapsed() >= Duration::from_millis(200) {
                        std::thread::sleep(Duration::from_micros(100));
                        last_callback_time = Instant::now();
                    }
                }
            }

            if !passwords.is_empty() && !found.load(Ordering::Relaxed) {
                let result_found = Self::process_batch_static(
                    &zip_path,
                    &passwords,
                    &actual_trys,
                    &found,
                    &result,
                )?;

                if result_found.is_some() {
                    return Ok(result_found);
                }
            }

            Ok(None)
        }).map_err(|e: String| PyIOError::new_err(e))?;

        if let Some(ref cb) = callback {
            let tries = actual_trys.load(Ordering::Relaxed);
            cb.call1(py, (tries,))?;
        }

        Ok(final_result)
    }

    #[getter]
    fn actual_trys(&self) -> u64 {
        self.get_tries()
    }
}

impl BruteForce {
    fn process_batch_static(
        zip_path: &str,
        passwords: &[String],
        actual_trys: &Arc<AtomicU64>,
        found: &Arc<AtomicBool>,
        result: &Arc<parking_lot::Mutex<Option<String>>>,
    ) -> Result<Option<String>, String> {
        let found_password = passwords.par_iter().find_map_any(|password| {
            if found.load(Ordering::Relaxed) {
                return None;
            }

            actual_trys.fetch_add(1, Ordering::Relaxed);

            let file = File::open(zip_path).ok()?;
            let mut archive = ZipArchive::new(file).ok()?;
            
            if archive.len() == 0 {
                return None;
            }

            let entry_result = archive.by_index_decrypt(0, password.as_bytes()).ok()?;
            let mut entry = entry_result.ok()?;
            let mut buffer = Vec::new();
            
            if entry.read_to_end(&mut buffer).is_ok() {
                Some(password.clone())
            } else {
                None
            }

        });

        if let Some(ref password) = found_password {
            found.store(true, Ordering::Relaxed);
            *result.lock() = Some(password.clone());
        }

        Ok(found_password)
    }
}

#[pymodule]
fn fast_zip(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<BruteForce>()?;
    m.add_function(wrap_pyfunction!(bruteforce_zip, m)?)?;
    Ok(())
}