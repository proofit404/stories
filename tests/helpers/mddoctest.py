from doctest import testfile
from sys import argv
from sys import exit


def _setup():
    pass


def _main():
    markdown_files = argv[1:]
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    exit(exit_code)


if __name__ == "__main__":  # pragma: no branch
    _setup()
    _main()
