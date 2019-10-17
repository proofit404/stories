import configparser
import subprocess

import pytest

tomlkit = pytest.importorskip("tomlkit")
yaml = pytest.importorskip("yaml")


def test_tox_environments_equal_azure_tasks():
    """
    Every tox environment should be precent in the Azure Pipeline task list.

    The order should be preserved.
    """

    tox_environments = [
        l.decode() for l in subprocess.check_output(["tox", "-l"]).splitlines()
    ]

    azure_pipelines = yaml.safe_load(open("azure-pipelines.yml").read())
    azure_tasks = [
        v["tox.env"] for v in azure_pipelines["jobs"][0]["strategy"]["matrix"].values()
    ]

    assert tox_environments == azure_tasks


def test_coverage_include_all_packages():
    """
    Coverage source should include packages:

    * from the main pyproject.toml,
    * from test helpers pyproject.toml,
    * the tests package
    """

    ini_parser = configparser.ConfigParser()
    ini_parser.read("setup.cfg")
    coverage_sources = ini_parser["coverage:run"]["source"].strip().splitlines()

    pyproject_toml = tomlkit.loads(open("pyproject.toml").read())
    package = [
        p["include"].rstrip(".py") for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    test_pyproject_toml = tomlkit.loads(open("tests/helpers/pyproject.toml").read())
    helpers = [
        p["include"].rstrip(".py")
        for p in test_pyproject_toml["tool"]["poetry"]["packages"]
    ]

    assert coverage_sources == package + helpers + ["tests"]
