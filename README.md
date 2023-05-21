# ZipCracker

[![Version](https://img.shields.io/badge/Version-1.o-green)]()
[![Bash](https://img.shields.io/badge/Made%20with-Python-blue)]()
[![License](https://img.shields.io/badge/License-GPL-yellow)]()

ZipCracker is a tool to crack .zip files passwords using wordlist files, see more at [usage](#usage) and [test files](#test-files) to use the tool correctly.

## INSTALLATION
### One line installation.
Just copy this line and paste in the terminal.
```bash
apt install -y git python; git clone https://github.com/TrollSkull/ZipCracker; cd easyTPKG; python zipcracker.py
```

You can download ZipCracker on any platform by cloning the official Git repository:

```bash
$ apt install -y git python

$ git clone https://github.com/TrollSkull/ZipCracker

$ cd ZipCracker

$ python translator.py or python zipcracker.py
```

## USAGE

To get a list of all options use the `--help` command.

```
usage: zipcracker.py file.zip -t 4 -f passwords.txt    

Zipfile cracker v1.0 by TrollSkull

positional arguments:
  zipfile               zip file name here.

options:
  -h, --help            show this help message and exit
  --passwfile PASSWFILE, -f PASSWFILE
                        if you have a password list for bruteforce, you can input using "-f passw.txt"
  --threads THREADS, -t THREADS
                        number of instances of python, this will use more CPU, I recommend a maximum of 4 threads
```

## TEST FILES

You can test `ZipCracker` speed and power by using the files in the `/test` folder, the correct password will be in row `73722`, you can test changing the number of threads with `-t` and see the speed changes when using different threads.

`python zipcracker.py test/test.zip -t 4 -f test/wordlist.txt`
    
### LICENCE

**[GPL 3-0 License © ZipCracker](https://github.com/TrollSkull/ZipCracker/blob/main/LICENSE)**
