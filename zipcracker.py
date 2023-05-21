__author__ = 'TrollSkull'
__version__ = '1.0'

try:
    import requests
    import pyzipper

except ImportError as error:
    import time, os

    print(str(error) + '\nSome requirements are not installed. \n')
    requirements = ['pyzipper', 'requests']

    for requirement in requirements:

        print(f'Installing "{requirement}"...')
        os.system(f'pip3 install {requirement}')
        time.sleep(1)

    print('\nRequirements have been installed.')

import threading
import requests
import pyzipper
import argparse
import datetime
import sys, os

parser = argparse.ArgumentParser(description='Zipfile bruteforce v1.0 by TrollSkull',
                                 usage="pwned.py file.zip -t 4 -f passwords.txt")

parser.add_argument('zipfile', help='zip file name here.')

parser.add_argument('--passwfile', '-f', type=str, required=True,
                    help='if you have a password list for bruteforce, you can input using "-f passw.txt"')

parser.add_argument('--threads', '-t', type=int, required=False,
                    help='number of instances of python, this will use more CPU, i recomend max 4 threads')

args = parser.parse_args()
start = datetime.datetime.now()

def check_zip(file):
    if not os.path.isfile(file):
        sys.exit(f'File "{file}" does not exist.')

    if not os.path.splitext(file)[1] == '.zip':
        sys.exit(f'File "{file}" is not a ZIP file.')

def extract_zip(zipfile, password_list, thread_index, num_threads):
    try:
        with pyzipper.AESZipFile(zipfile) as zf:

            global trys
            trys = 0

            for password in password_list:
                trys += 1
                try:
                    password = password.strip()
                    zf.pwd = password
                    zf.extractall()

                    print(f"Zip file unlocked with password: {password.decode('utf-8')}")
                    sys.exit(0)

                except RuntimeError:
                    continue

    except pyzipper.zipfile.BadZipFile as error:
        print(str(error))
        sys.exit(1)

def run_threads(zipfile, passwords, num_threads):
    chunk_size = len(passwords) // num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(passwords)
        password_chunk = passwords[start:end]

        t = threading.Thread(target=extract_zip, args=(zipfile, password_chunk, i, num_threads))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def main():
    check_zip(args.zipfile)

    with open(args.passwfile, 'rb') as f:
        passwords = f.readlines()

    num_threads = args.threads if args.threads else 1
    run_threads(args.zipfile, passwords=passwords, num_threads=num_threads)
    
if __name__ == '__main__':
    main()
    
    finish = datetime.datetime.now()
    total = int((finish - start).total_seconds())
    print(f'It took {total} seconds to decipher, {trys} attempts in total')
