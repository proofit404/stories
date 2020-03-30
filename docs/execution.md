# Execution rules

`stories` follow this executing rules to run:

- Methods of the class will be called in the order as they were
  written in the story
- If the story calls another story in its body, methods of this
  sub-story add to the caller in the order they occur in sub-story
  body.
- Each story method should return an instance of `Success`, `Failure`,
  `Result` or `Skip` classes.
- The execution of the story will change according to the type of the
  return value.

## Success

If the story method returns `Success` execution of the whole story
continues from the next step.

```pycon tab="sync"

>>> from stories import story, Success

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...         I.three
...
...     def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     def two(self, ctx):
...
...         print("two")
...         return Success()
...
...     def three(self, ctx):
...
...         print("three")
...         return Success()

>>> Action().do()
one
two
three

```

```pycon tab="async"

>>> from stories import story, Success

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...         I.three
...
...     async def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Success()
...
...     async def three(self, ctx):
...
...         print("three")
...         return Success()

>>> await Action().do()  # doctest: +SKIP
one
two
three

```

If sub-story last method returns `Success`, the execution continues in
the next method of the parent story.

```pycon tab="sync"

>>> from stories import story, Success

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     def two(self, ctx):
...
...         print("two")
...         return Success()
...
...     def three(self, ctx):
...
...         print("three")
...         return Success()
...
...     def four(self, ctx):
...
...         print("four")
...         return Success()

>>> Action().do()
one
two
three
four

```

```pycon tab="async"

>>> from stories import story, Success

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     async def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Success()
...
...     async def three(self, ctx):
...
...         print("three")
...         return Success()
...
...     async def four(self, ctx):
...
...         print("four")
...         return Success()

>>> await Action().do()  # doctest: +SKIP
one
two
three
four

```

Story method can assign attributes to the context to set some
variables for future methods.

```pycon tab="sync"

>>> from stories import story, Success

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...
...     def one(self, ctx):
...
...         ctx.var_a = 1
...         ctx.var_b = 2
...         return Success()
...
...     def two(self, ctx):
...
...         print(ctx.var_a)
...         print(ctx.var_b)
...         return Success()

>>> Action().do()
1
2

```

```pycon tab="async"

>>> from stories import story, Success

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...
...     async def one(self, ctx):
...
...         ctx.var_a = 1
...         ctx.var_b = 2
...         return Success()
...
...     async def two(self, ctx):
...
...         print(ctx.var_a)
...         print(ctx.var_b)
...         return Success()

>>> await Action().do()  # doctest: +SKIP
1
2

```

!!! note

    A previous version of the stories library implemented the same
    behavior with `Success()` marker keyword arguments.  If you need
    to migrate source files where outdated version of the library was
    used, please have a look at the
    [editors](https://github.com/dry-python/editors#stories-upgrade)
    project.  It will refactory all your codebase properly within a
    single command.

## Failure

If story method returns `Failure`, the whole story considered failed.
Execution stops at this point.

```pycon tab="sync"

>>> from stories import story, Success, Failure

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...
...     def one(self, ctx):
...
...         print("one")
...         return Failure()
...
...     def two(self, ctx):
...
...         print("two")
...         return Success()

>>> result = Action().do.run()
one

>>> result.is_failure
True

```

```pycon tab="async"

>>> from stories import story, Success, Failure

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...
...     async def one(self, ctx):
...
...         print("one")
...         return Failure()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Success()

>>> result = await Action().do.run()  # doctest: +SKIP
one

>>> result.is_failure
True

```

`Failure` of the sub-story will fail the whole story.

```pycon tab="sync"

>>> from stories import story, Success, Failure

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     def two(self, ctx):
...
...         print("two")
...         return Failure()
...
...     def three(self, ctx):
...
...         print("three")
...         return Success()
...
...     def four(self, ctx):
...
...         print("four")
...         return Success()

>>> result = Action().do.run()
one
two

>>> result.is_failure
True

```

```pycon tab="async"

>>> from stories import story, Success, Failure

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     async def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Failure()
...
...     async def three(self, ctx):
...
...         print("three")
...         return Success()
...
...     async def four(self, ctx):
...
...         print("four")
...         return Success()

>>> result = await Action().do.run()  # doctest: +SKIP
one
two

>>> result.is_failure
True

```

`Failure` has optional `reason` argument. We describe it in details in
the [failure protocol](failure_protocol.md) chapter.

## Result

If the story method return `Result`, the whole story considered done. An
optional argument passed to the `Result` constructor will be the return
value of the story call.

```pycon tab="sync"

>>> from stories import story, Success, Result

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...         I.three
...
...     def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     def two(self, ctx):
...
...         print("two")
...         return Result(1)
...
...     def three(self, ctx):
...
...         print("three")
...         return Success()

>>> res = Action().do()
one
two

>>> res
1

```

```pycon tab="async"

>>> from stories import story, Success, Result

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...         I.three
...
...     async def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Result(1)
...
...     async def three(self, ctx):
...
...         print("three")
...         return Success()

>>> res = await Action().do()  # doctest: +SKIP
one
two

>>> res
1

```

The `Result` of the sub-story will be the result of the whole story. The
execution stops after the method returned `Result`.

```pycon tab="sync"

>>> from stories import story, Success, Result

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     def two(self, ctx):
...
...         print("two")
...         return Success()
...
...     def three(self, ctx):
...
...         print("three")
...         return Result(2)
...
...     def four(self, ctx):
...
...         print("four")
...         return Success()

>>> result = Action().do()
one
two
three

>>> result
2

```

```pycon tab="async"

>>> from stories import story, Success, Result

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     async def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Success()
...
...     async def three(self, ctx):
...
...         print("three")
...         return Result(2)
...
...     async def four(self, ctx):
...
...         print("four")
...         return Success()

>>> result = await Action().do()  # doctest: +SKIP
one
two
three

>>> result
2

```

## Skip

If sub-story method returns `Skip` result, execution will be continued
form the next method of the caller story.

```pycon tab="sync"

>>> from stories import story, Success, Skip

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     def two(self, ctx):
...
...         print("two")
...         return Skip()
...
...     def three(self, ctx):
...
...         print("three")
...         return Success()
...
...     def four(self, ctx):
...
...         print("four")
...         return Success()

>>> Action().do()
one
two
four

```

```pycon tab="async"

>>> from stories import story, Success, Skip

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.sub
...         I.four
...
...     @story
...     def sub(I):
...
...         I.two
...         I.three
...
...     async def one(self, ctx):
...
...         print("one")
...         return Success()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Skip()
...
...     async def three(self, ctx):
...
...         print("three")
...         return Success()
...
...     async def four(self, ctx):
...
...         print("four")
...         return Success()

>>> await Action().do()  # doctest: +SKIP
one
two
four

```

If the topmost story returns `Skip` result, execution will end.

```pycon tab="sync"

>>> from stories import story, Success, Skip

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...
...     def one(self, ctx):
...
...         print("one")
...         return Skip()
...
...     def two(self, ctx):
...
...         print("two")
...         return Success()

>>> Action().do()
one

```

```pycon tab="async"

>>> from stories import story, Success, Skip

>>> class Action:
...
...     @story
...     def do(I):
...
...         I.one
...         I.two
...
...     async def one(self, ctx):
...
...         print("one")
...         return Skip()
...
...     async def two(self, ctx):
...
...         print("two")
...         return Success()

>>> await Action().do()  # doctest: +SKIP
one

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>Drylabs maintains dry-python and helps those who want to use it inside their organizations.</i></p>
<p align="center"><i>Read more at <a href="https://drylabs.io">drylabs.io</a></i></p>
