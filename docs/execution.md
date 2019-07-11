# Execution rules

`stories` follow this executing rules to run:

* Methods of the class will be called in the order as they were
  written in the story
* If the story calls another story in its body, methods of this
  sub-story add to the caller in the order they occur in sub-story
  body.
* Each story method should return an instance of `Success`, `Failure`,
  `Result` or `Skip` classes.
* The execution of the story will change according to the type of the
  return value.

## Success

If the story method returns `Success` execution of the whole story
continues from the next step.

```pycon

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

```

```pycon

>>> Action().do()
one
two
three

```

If sub-story last method returns `Success`, the execution continues in
the next method of the parent story.

```pycon

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

```

```pycon

>>> Action().do()
one
two
three
four

```

Story method can use `Success` keyword arguments to set some context
variables for future methods.

```pycon

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
...         return Success(var_a=1, var_b=2)
...
...     def two(self, ctx):
...
...         print(ctx.var_a)
...         print(ctx.var_b)
...         return Success()

```

```pycon

>>> Action().do()
1
2

```

## Failure

If story method returns `Failure`, the whole story considered failed.
Execution stops at this point.

```pycon

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

```

```pycon

>>> Action().do()
one
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "stories/_wrapper.py", line 23, in __call__
    return function.execute(runner, ctx, methods)
  File "stories/_exec/function.py", line 33, in execute
    return runner.got_failure(ctx, method.__name__, result.reason)
  File "stories/_run.py", line 7, in got_failure
    raise FailureError(reason)
stories.exceptions.FailureError()

```

`Failure` of the sub-story will fail the whole story.

```pycon

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

```

```pycon

>>> Action().do()
one
two
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "stories/_wrapper.py", line 23, in __call__
    return function.execute(runner, ctx, methods)
  File "stories/_exec/function.py", line 33, in execute
    return runner.got_failure(ctx, method.__name__, result.reason)
  File "stories/_run.py", line 7, in got_failure
    raise FailureError(reason)
stories.exceptions.FailureError()

```

`Failure` has optional `reason` argument. We describe it in details in
the [failure protocol](failure_protocol.md) chapter.

## Result

If the story method return `Result`, the whole story considered done. An
optional argument passed to the `Result` constructor will be the return
value of the story call.

```pycon

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

```

```pycon

>>> res = Action().do()
one
two
>>> res
1

```

The `Result` of the sub-story will be the result of the whole story. The
execution stops after the method returned `Result`.

```pycon

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

```

```pycon

>>> result = Action().do()
one
two
three
>>> result
2

```

## Skip

If sub-story method returns `Skip` result, execution will be continued
form the next method of the caller story.

```pycon

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

```

```pycon

>>> Action().do()
one
two
four

```

If the topmost story returns `Skip` result, execution will end.

```pycon

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

```

```pycon

>>> Action().do()
one

```
