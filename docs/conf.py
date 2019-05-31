#!/usr/bin/env python3

project = "stories"

copyright = "2018-2019, dry-python team"

author = "Artem Malyshev"

version = "0.10.1"

release = "0.10.1"

templates_path = ["templates"]

source_suffix = ".rst"

master_doc = "index"

language = None

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "alabaster"

html_static_path = ["static"]

html_sidebars = {
    "**": [
        "sidebarlogo.html",
        "stats.html",
        "globaltoc.html",
        "relations.html",
        "updates.html",
        "links.html",
        "searchbox.html",
        "image_popup.html",
        "gitter_sidecar.html",
    ]
}

html_theme_options = {
    "show_powered_by": False,
    "show_related": True,
    "show_relbars": True,
    "description": "Business transaction DSL.  It provides a simple way to define a complex business transaction that includes processing by many different objects.",  # noqa: E501
    "github_user": "dry-python",
    "github_repo": "stories",
    "github_type": "star",
    "github_count": True,
    "github_banner": True,
}
