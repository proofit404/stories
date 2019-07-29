import sys
from doctest import testfile
from glob import glob
from unittest.mock import Mock

from django.apps import apps
from django.conf import settings

from stories import Success, Failure, Result, arguments, story


def main():
    apps.populate(settings.INSTALLED_APPS)
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file,
                                     module_relative=False,
                                     globs={
                                         'Profile': Mock(),
                                         'Price': Mock(),
                                         'Success': Success,
                                         'Failure': Failure,
                                         'Result': Result,
                                         'arguments': arguments,
                                         'story': story
                                         }
                                     )
        exit_code += failed
    sys.exit(exit_code)
