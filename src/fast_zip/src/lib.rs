use pyo3::prelude::*;
use rayon::prelude::*;
use std::fs::File;
use std::io::Read;
use zip::ZipArchive;

#[pyfunction]
fn bruteforce_zip(zip_path: &str, passwords: Vec<String>) -> Option<String> {
    passwords.par_iter().find_map_any(|password| {
        let file = File::open(zip_path).ok()?;
        let mut archive = ZipArchive::new(file).ok()?;

        let entry_result = archive.by_index_decrypt(0, password.as_bytes()).ok()?;

        let mut entry = entry_result.ok()?;

        let mut buffer = Vec::new();
        entry.read_to_end(&mut buffer).ok()?;

        Some(password.clone())
    })
}

#[pymodule]
fn fast_zip(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(bruteforce_zip, m)?)?;
    Ok(())
}
