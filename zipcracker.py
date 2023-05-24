__author__ = 'TrollSkull'
__version__ = '2.0'

from concurrent.futures import ThreadPoolExecutor, wait
import threading
import datetime
import argparse
import zipfile
import sys
import os

parser = argparse.ArgumentParser(description='Zipfile cracker v1.0 by TrollSkull',
                                 usage="zipcracker.py file.zip -t 4 -w wordlist.txt")

parser.add_argument('zipfile', help='zip file name here.')

parser.add_argument('--wordlist', '-w', type=str, required=True,
                    help='if you have a wordlist list for bruteforce, you can input using "-w wordlist.txt"')

parser.add_argument('--threads', '-t', type=int, required=False,
                    help='number of instances of python, this will use more CPU, I recommend a maximum of 4 threads')

args = parser.parse_args()
start = datetime.datetime.now()
trys = 0
verified_passwords = set()

def check_zip(file):
    if not os.path.isfile(file):
        sys.exit(f'File "{file}" does not exist.')

    if not os.path.splitext(file)[1] == '.zip':
        sys.exit(f'File "{file}" is not a ZIP file.')

def extract_zip(zip_file, password_list):
    global trys

    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            for password in password_list:
                if found_password.is_set():
                    break

                try:
                    password = password.strip().decode('utf-8')
                    zf.extractall(path=None, pwd=password.encode('utf-8'))

                    with results_lock:
                        found_password.set()
                        finish = datetime.datetime.now()
                        total = int((finish - start).total_seconds())

                        print(f'\nZip file unlocked with password: {password}')
                        print(f'It took {total} seconds to decipher, {trys} attempts in total.')

                    return password

                except Exception:
                    continue

                finally:
                    trys += 1
                    if password not in verified_passwords:
                        verified_passwords.add(password)

                        sys.stdout.write(f"\rVerified passwords: {trys}")
                        sys.stdout.flush()

    except zipfile.BadZipFile as error:
        print(str(error))
        sys.exit(1)

def run_threads(zip_file, passwords, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        chunk_size = (len(passwords) + num_threads - 1) // num_threads
        password_chunks = [passwords[i:i+chunk_size] for i in range(0, len(passwords), chunk_size)]
        futures = []

        for password_chunk in password_chunks:
            future = executor.submit(extract_zip, zip_file, password_chunk)
            futures.append(future)

        done, _ = wait(futures, return_when='FIRST_COMPLETED')

        for future in done:
            if future.done() and future.result() is not None:
                break

def main():
    check_zip(args.zipfile)

    if not os.path.isfile(args.wordlist):
        sys.exit(f'File "{args.wordlist}" does not exist.')

    with open(args.wordlist, 'rb') as f:
        passwords = f.readlines()

    num_threads = args.threads if args.threads else 1
    run_threads(args.zipfile, passwords, num_threads)

if __name__ == '__main__':
    found_password = threading.Event()
    results_lock = threading.Lock()

    main()
