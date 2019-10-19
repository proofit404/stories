import configparser
import json
import subprocess

import pytest

# This is a little bit a workaround of the PyYaml library limitations.
# It doesn't preserve the order of keys of the parsed dict.  It works
# on recent Python versions where the order of keys is guaranteed by
# dict implementation.  We do not install necessary libraries for the
# test, so it does not fail because it does not run.  See
# https://github.com/yaml/pyyaml/issues/110 for more info.
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


def test_tox_deps_are_ordered():
    """
    Dependencies section of all tox environments should be in alphabetical order.
    """

    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if "deps" in ini_parser[section]:
            deps = ini_parser[section]["deps"].strip().splitlines()
            ordered = [
                deps[l[-1]]
                for l in sorted(
                    [
                        (*map(lambda x: x.strip().lower(), reversed(d.split(":"))), i)
                        for i, d in enumerate(deps)
                    ],
                    key=lambda key: (key[0], key[1]),
                )
            ]
            assert deps == ordered


def test_nodejs_deps_are_ordered():
    """
    Development dependencies of the package.json should be in alphabetical order.
    """

    package_json = json.load(open("package.json"))
    deps = list(package_json["devDependencies"].keys())
    assert deps == sorted(deps)


def test_packages_are_ordered():
    """
    Packages section of all pyproject.toml files should be in alphabetical order.
    """

    for pyproject_toml in ["pyproject.toml", "tests/helpers/pyproject.toml"]:
        pyproject_toml = tomlkit.loads(open(pyproject_toml).read())
        packages = [
            p["include"].rstrip(".py")
            for p in pyproject_toml["tool"]["poetry"]["packages"]
        ]
        assert packages == sorted(packages)


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
    packages = [
        p["include"].rstrip(".py") for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    pyproject_toml = tomlkit.loads(open("tests/helpers/pyproject.toml").read())
    helpers = [
        p["include"].rstrip(".py") for p in pyproject_toml["tool"]["poetry"]["packages"]
    ]

    assert coverage_sources == packages + helpers + ["tests"]
