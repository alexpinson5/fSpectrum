import subprocess
import sys
import importlib.util

# Function to check if a package is part of the standard library
def is_standard_package(package_name):
    standard_packages = [
        'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 
        'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'calendar', 
        'cgi', 'cgitb', 'chunk', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 
        'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt', 
        'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 
        'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 
        'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 
        'gettext', 'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 
        'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 
        'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 
        'multiprocessing', 'netrc', 'nntplib', 'numbers', 'operator', 'optparse', 'os', 'pathlib', 'pdb', 
        'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'pprint', 
        'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 
        're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 
        'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 
        'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 
        'symbol', 'symtable', 'sys', 'sysconfig', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 
        'textwrap', 'this', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 
        'tracemalloc', 'tty', 'turtle', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 
        'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 
        'zipfile', 'zipimport', 'zlib'
    ]
    return package_name in standard_packages

# Function to check and install packages
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

def check_and_install_packages(packages):
    for package in packages:
        if is_standard_package(package):
            # Import standard library packages
            __import__(package)
        else:
            install_and_import(package)