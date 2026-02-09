import PyInstaller.__main__

def build_executable():
    PyInstaller.__main__.run([
        '--add-data=src/assets;assets',
        '-i', 'src/assets/icon.ico',
        '--noconsole',
        f'--name=ZipCracker-v3.0-x64',
        '--onedir',
        '--clean',
        'src/main.py'
    ])

if __name__ == "__main__":
    build_executable()