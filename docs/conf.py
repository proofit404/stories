#!/usr/bin/env python3

project = "stories"

copyright = "2018, Artem Malyshev"

author = "Artem Malyshev"

version = "0.8"

release = "0.8"

templates_path = ["templates"]

source_suffix = ".rst"

master_doc = "index"

language = None

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "alabaster"

html_static_path = ["static"]

html_theme_options = {
    "show_related": True,
    "github_user": "dry-python",
    "github_repo": "stories",
    "github_banner": True,
}
