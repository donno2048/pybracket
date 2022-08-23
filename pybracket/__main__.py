from sys import argv
try:
    from . import main as register
except ImportError:
    from pybracket import main as register
def main():
    register()
    if len(argv) == 1:
        raise Exception("No file passed to execute")
    exec(open(argv[1], "rb").read().decode("brackets"))
if __name__ == '__main__':
    main()
