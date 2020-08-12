## [1.0.2](https://github.com/proofit404/stories/compare/1.0.1...1.0.2) (2020-07-31)

### Bug Fixes

- deny to use same story step twice
  ([d379956](https://github.com/proofit404/stories/commit/d379956db8d4cc1e4a0b3e55872f9ad051d8a29a))

## [1.0.1](https://github.com/proofit404/stories/compare/1.0.0...1.0.1) (2020-06-26)

### Bug Fixes

- prevent story to call itself recursively
  ([4a7007a](https://github.com/proofit404/stories/commit/4a7007a928713661ba73f9bf1edc509e3b3363a5))

# [1.0.0](https://github.com/proofit404/stories/compare/0.15.0...1.0.0) (2020-05-22)

### Features

- deprecate substories defined within the class
  ([c5d7930](https://github.com/proofit404/stories/commit/c5d7930af4d0af3a510993b852aeee19335a4154)),
  closes [#388](https://github.com/proofit404/stories/issues/388)

### BREAKING CHANGES

- Substories defined in the same class do not deserve special treatment. From
  now they require to have different context contracts and failure protocols.
  They will be interpreted the same way as if they were defined in the other
  class. Shortcuts module have been removed.

# [0.15.0](https://github.com/proofit404/stories/compare/0.14.0...0.15.0) (2020-04-16)

### Features

- support Django 4.0
  ([f02a334](https://github.com/proofit404/stories/commit/f02a3341c58b7885a2095c11ff5bef4acf626e94))

# [0.14.0](https://github.com/proofit404/stories/compare/0.13.0...0.14.0) (2020-03-21)

### Features

- support marshmallow v3 as a context contract definition
  ([a87c0c4](https://github.com/proofit404/stories/commit/a87c0c45cbb52e40fba872f57aa07a3550de6143))

# [0.13.0](https://github.com/proofit404/stories/compare/0.12.0...0.13.0) (2020-03-14)

### Features

- use assignment expression instead of Success keyword arguments
  ([9756571](https://github.com/proofit404/stories/commit/9756571237d56c52f8769c61f20f544ab389a211))

# [0.12.0](https://github.com/proofit404/stories/compare/0.11.2...0.12.0) (2020-03-06)

### Features

- support coroutine functions as story step definitions
  ([55cbfda](https://github.com/proofit404/stories/commit/55cbfda33c61ca1395aaacf2d2d6a2c78f14ecde))

## [0.11.2](https://github.com/proofit404/stories/compare/0.11.1...0.11.2) (2020-03-02)

### Bug Fixes

- hide context private attributes in closure
  ([f8144aa](https://github.com/proofit404/stories/commit/f8144aabd8629682f9c7368a23c80316bb10fddc))
- hide failure and success summary private attributes in closure
  ([eae4e95](https://github.com/proofit404/stories/commit/eae4e95bd89a2df8fd31f77fe665659c29feedd8))
- hide FailureError private attributes in closure
  ([1fafcc1](https://github.com/proofit404/stories/commit/1fafcc1039775f2fbcc242b582181fab2d4e63d7))
- hide story private attributes in closure
  ([9e79e14](https://github.com/proofit404/stories/commit/9e79e1417785db1e13ed01a1cd64613d5bf24a8a))

## [0.11.1](https://github.com/proofit404/stories/compare/0.11.0...0.11.1) (2020-02-28)

### Bug Fixes

- deny to define stories without steps
  ([5067546](https://github.com/proofit404/stories/commit/5067546386df294db595fb0ee4e8968ee295c4b3))

# [0.11.0](https://github.com/proofit404/stories/compare/0.10.2...0.11.0) (2020-02-14)

### Features

- Add context contract to the story. `Success` keyword arguments can be
  validated by contract definition in the story.
- Raise `MutationError` when some story method tries to set or delete context
  attribute directly.
- Only keyword arguments are allowed to `call` and `run` the story.
- Raise `StoryDefinitionError` when `arguments` decorator is used incorrectly.
- migrate to pydantic v1.x
  ([9049eae](https://github.com/proofit404/stories/commit/9049eae43c7b8db36708fc019a671a53bf4b578d))

## [0.10.2](https://github.com/proofit404/stories/compare/0.10.1...0.10.2) (2020-02-11)

### Bug Fixes

- prevent generated changelog from style guide violation
  ([7d4047d](https://github.com/proofit404/stories/commit/7d4047d10e4dacc10ec356700b1fc35161efa4c0))

## 0.10.1 (2019-05-31)

- Fix pytest reporter to work with fixture functions and `pytest-bdd` plugin
  properly.

## 0.10 (2019-02-27)

- Add failure protocol of the story. `Failure` argument should match protocol
  definition in the story.
- Replace multiple `argument` decorators with single `arguments`.
- Raise `ContextContractError` when keyword argument given to `Success` already
  exists in the context.
- Raise `ContextContractError` when the story can not find necessary arguments
  in the context.
- Make context an immutable object.
- Python 3.7 support.

## 0.9 (2018-11-28)

- Enforce `I` noun with non callable attributes in the story definition.
- `Context` is passed as an argument into story step methods.
- Pass real class instances into step method.
- Show story execution path in the `Context` representation.
- Add Sentry, Py.test and Django Debug Toolbar plugins with `Context` reporter
  built in.
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
- `Skip` result was added to finish nested stories without finish the caller.

## 0.0.3 (2018-04-06)

- Nested stories support.

## 0.0.2 (2018-04-03)

- Fix class and instance attribute access.
- Validate return values.
- Make context append only.

## 0.0.1 (2018-04-02)

- Initial release.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The stories library is part of the SOLID python family.</i></p>
