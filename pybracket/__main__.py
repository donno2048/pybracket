from sys import argv
def main():
    if len(argv) == 1:
        raise Exception("No file passed to execute")
    exec(open(argv[1], "rb").read().decode("brackets"))
if __name__ == '__main__':
    main()
