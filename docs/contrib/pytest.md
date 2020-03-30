# Py.Test contrib

![Py.Test Report](https://raw.githubusercontent.com/dry-python/dry-python.github.io/develop/slides/pics/pytest.png)

Py.test plugin provides an additional report for failed tests. It
contains:

1. Stories started by the failed test is chronological order.
2. Exact execution path for each story.
3. A context for each story.
4. Corresponding source line of the test started each story.

This plugin is enabled by default.

To disable it add `-p no:stories` argument to the `pytest` command.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
