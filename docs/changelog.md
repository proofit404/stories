# [0.11.0](https://github.com/dry-python/stories/compare/0.10.2...0.11.0) (2020-02-14)

### Features

- Add context contract to the story. `Success` keyword arguments can
  be validated by contract definition in the story.
- Raise `MutationError` when some story method tries to set or delete
  context attribute directly.
- Only keyword arguments are allowed to `call` and `run` the story.
- Raise `StoryDefinitionError` when `arguments` decorator is used
  incorrectly.
- migrate to pydantic v1.x ([9049eae](https://github.com/dry-python/stories/commit/9049eae43c7b8db36708fc019a671a53bf4b578d))

## [0.10.2](https://github.com/dry-python/stories/compare/0.10.1...0.10.2) (2020-02-11)

### Bug Fixes

- prevent generated changelog from style guide violation ([7d4047d](https://github.com/dry-python/stories/commit/7d4047d10e4dacc10ec356700b1fc35161efa4c0))

## 0.10.1 (2019-05-31)

- Fix pytest reporter to work with fixture functions and `pytest-bdd`
  plugin properly.

## 0.10 (2019-02-27)

- Add failure protocol of the story. `Failure` argument should match
  protocol definition in the story.
- Replace multiple `argument` decorators with single `arguments`.
- Raise `ContextContractError` when keyword argument given to
  `Success` already exists in the context.
- Raise `ContextContractError` when the story can not find necessary
  arguments in the context.
- Make context an immutable object.
- Python 3.7 support.

## 0.9 (2018-11-28)

- Enforce `I` noun with non callable attributes in the story
  definition.
- `Context` is passed as an argument into story step methods.
- Pass real class instances into step method.
- Show story execution path in the `Context` representation.
- Add Sentry, Py.test and Django Debug Toolbar plugins with `Context`
  reporter built in.
- Raise an exception on `Failure` when the story was called directly.
- Support iterable protocol in the `Context` class.
- Add `Failure` reason.
- Fix `Skip` result behavior in deeper sub-story hierarchy.

## 0.8 (2018-05-12)

- Add `dir()` and `repr()` support to the context class.
- Failed result holds a link to the context.

## 0.7 (2018-05-06)

- Add `run` interface to the story.

## 0.6 (2018-04-19)

- Representation methods for story, context and point result classes.
- Python 2 support.

## 0.5 (2018-04-07)

- Do not execute nested stories of the skipped story.

## 0.4 (2018-04-07)

- Package was rewritten with linearization algorithm.
- `Skip` result was added to finish nested stories without finish the
  caller.

## 0.0.3 (2018-04-06)

- Nested stories support.

## 0.0.2 (2018-04-03)

- Fix class and instance attribute access.
- Validate return values.
- Make context append only.

## 0.0.1 (2018-04-02)

- Initial release.
