# ZipCracker

[![Version](https://img.shields.io/badge/Version-2.0-green)]()
[![Bash](https://img.shields.io/badge/Made%20with-Python-blue)]()
[![License](https://img.shields.io/badge/License-GPL-yellow)]()

### Table of content.
1. [Disclaimer](#disclaimer)
2. [Installation](#installation)
3. [Wordlist](#wordlist)
4. [Usage](#usage)
5. [Test Files](#testfiles)
6. [License](#license)

ZipCracker is a tool to crack .zip files passwords using wordlist files, see more at [usage](#usage) and [test files](#test-files) to use the tool correctly.

## Disclaimer
This script is not made with malicious intent, it was built for educational purposes, to understand how zip crackers work and to provide one with free and clean code :}

## INSTALLATION
### One line installation.
Just copy this line and paste in the terminal.
```bash
apt install -y git python; git clone https://github.com/TrollSkull/ZipCracker; cd ZipCracker; python zipcracker.py
```

You can download ZipCracker on any platform by cloning the official Git repository:

```bash
$ apt install -y git python

$ git clone https://github.com/TrollSkull/ZipCracker

$ cd ZipCracker

$ python translator.py or python zipcracker.py
```

## WORDLIST
You can download a wordlist with over 14 million passwords **[here](https://github.com/TrollSkull/ZipCracker/releases/download/wordlist/wordlist.txt)**.

## USAGE

To get a list of all options use the `--help` command.

```
usage: zipcracker.py file.zip -t 4 -w wordlist.txt    

Zipfile cracker v1.0 by TrollSkull

positional arguments:
  zipfile               zip file name here.

options:
  -h, --help            show this help message and exit
  --wordlist WORDLIST, -w WORDLIST
                        if you have a wordlist list for bruteforce, you can input using "-w wordlist.txt"
  --threads THREADS, -t THREADS
                        number of instances of python, this will use more CPU, I recommend a maximum of 4 threads
```

## TEST FILES

You can test `ZipCracker` speed and power by using the files in the `/test` folder, the correct password will be in row `73722`, you can test changing the number of threads with `-t` and see the speed changes when using different threads.

```bash
python zipcracker.py test/test.zip -t 4 -f test/wordlist.txt
```

### LICENSE

**[GPL 3-0 License © ZipCracker](https://github.com/TrollSkull/ZipCracker/blob/main/LICENSE)**
