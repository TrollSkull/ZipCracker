__author__ = 'TrollSkull'
__version__ = '1.0'

try:
    import pyzipper
    import requests
except ImportError:
    import os

    requirements = ['requests', 'pyzipper']

    for requirement in requirements:
        os.system(f'pip install {requirement}')

from concurrent.futures import ThreadPoolExecutor
import requests
import argparse
import pyzipper
import datetime
import sys
import os

parser = argparse.ArgumentParser(description='Zipfile cracker v1.0 by TrollSkull',
                                 usage="zipcracker.py file.zip -t 4 -f passwords.txt")

parser.add_argument('zipfile', help='zip file name here.')

parser.add_argument('--passwfile', '-f', type=str, required=True,
                    help='if you have a password list for bruteforce, you can input using "-f passw.txt"')

parser.add_argument('--threads', '-t', type=int, required=False,
                    help='number of instances of python, this will use more CPU, I recommend a maximum of 4 threads')

args = parser.parse_args()
start = datetime.datetime.now()
trys = 0

def check_zip(file):
    if not os.path.isfile(file):
        sys.exit(f'File "{file}" does not exist.')

    if not os.path.splitext(file)[1] == '.zip':
        sys.exit(f'File "{file}" is not a ZIP file.')

def extract_zip(zipfile, password_list, thread_index):
    global trys

    try:
        with pyzipper.AESZipFile(zipfile) as zf:
            for password in password_list:
                try:
                    password = password.strip()
                    zf.pwd = password
                    zf.extractall(pwd=password)

                    print(f"Zip file unlocked with password: {password.decode('utf-8')}")
                    sys.exit(0)

                except Exception:
                    continue

                finally:
                    trys += 1

    except pyzipper.zipfile.BadZipFile as error:
        print(str(error))
        sys.exit(1)

def run_threads(zipfile, passwords, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        chunk_size = (len(passwords) + num_threads - 1) // num_threads
        password_chunks = [passwords[i:i+chunk_size] for i in range(0, len(passwords), chunk_size)]

        for i, password_chunk in enumerate(password_chunks):
            executor.submit(extract_zip, zipfile, password_chunk, i)

def main():
    check_zip(args.zipfile)

    if not os.path.isfile(args.passwfile):
        sys.exit(f'File "{args.passwfile}" does not exist.')

    with open(args.passwfile, 'rb') as f:
        passwords = f.readlines()

    num_threads = args.threads if args.threads else 1
    run_threads(args.zipfile, passwords=passwords, num_threads=num_threads)

if __name__ == '__main__':
    main()

finish = datetime.datetime.now()
total = int((finish - start).total_seconds())
print(f'It took {total} seconds to decipher, {trys} attempts in total.')
