from doctest import testfile
from glob import glob
from sys import exit


def _setup():
    pass


def _main():
    exit_code = 0
    for markdown_file in glob("docs/**/*.md", recursive=True):
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    exit(exit_code)


if __name__ == "__main__":  # pragma: no branch
    _setup()
    _main()
