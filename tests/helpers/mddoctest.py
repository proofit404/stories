import sys
from doctest import testfile
from glob import glob
from types import ModuleType

from django.apps import apps
from django.conf import settings
from django.core import management


pdb = ModuleType("pdb")
pdb.pm = lambda: print(  # FIXME: Run real pdb.
    """
> example.py(73)apply_discount()
-> return price * self.fraction
(Pdb) ll
 71      def apply_discount(self, price):
 72
 73  ->      return price * self.fraction
(Pdb) args
self = <example.PromoCode>
price = None
    """.strip()
)


def main():
    apps.populate(settings.INSTALLED_APPS)
    management.call_command("migrate")
    management.call_command("loaddata", "examples.yaml")
    sys.modules["pdb"] = pdb
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
