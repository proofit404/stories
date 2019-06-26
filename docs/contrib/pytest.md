# Py.Test contrib

![image](/static/pytest.png)

Py.test plugin provides an additional report for failed tests. It
contains:

1. Stories started by the failed test is chronological order.
2. Exact execution path for each story.
3. A context for each story.
4. Corresponding source line of the test started each story.

This plugin is enabled by default.

To disable it add `-p no:stories` argument to the `pytest` command.
