
.. :changelog:

Changelog
---------

0.9.0 (2018-00-00)
++++++++++++++++++

- ``Proxy`` class ``repr()`` will show current execution path.
- Py.test plugin with context and execution path reporter.
- Raise exception on ``Failure`` when story was called directly.

0.8.0 (2018-05-12)
++++++++++++++++++

- Add ``dir()`` and ``repr()`` support to the context class.
- Failed result holds a link to the context.

0.7.0 (2018-05-06)
++++++++++++++++++

- Add ``run`` interface to the story.

0.6.0 (2018-04-19)
++++++++++++++++++

- Representation methods for story, context and point result classes.
- Python 2 support.

0.5.0 (2018-04-07)
++++++++++++++++++

- Do not execute nested stories of the skipped story.

0.4.0 (2018-04-07)
++++++++++++++++++

- Package was rewritten with linearization algorithm.
- ``Skip`` result was added to finish nested stories without finish
  the caller.

0.0.3 (2018-04-06)
++++++++++++++++++

- Nested stories support.

0.0.2 (2018-04-03)
++++++++++++++++++

- Fix class and instance attribute access.
- Validate return values.
- Make context append only.

0.0.1 (2018-04-02)
++++++++++++++++++

- Initial release.
