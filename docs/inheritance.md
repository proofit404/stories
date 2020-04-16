# Inheritance

We usually prefer [composition](composition.md) over inheritance.
This is a [well established principle](https://en.wikipedia.org/wiki/Composition_over_inheritance) from
the book [_Design Patterns: Elements of Reusable Object-Oriented Software_](https://en.wikipedia.org/wiki/Design_Patterns)
which was first published in 1994.

However, in some cases it is still preferable to use inheritance.
Whenever you can say that `A is a B`, inheritance is preferable.
For example a metal door **is a** door so if we where to create a `MetalDoor` class
it would certainly inherit from a `Door` base class.

To the contrary, if you can't say that `A is a B` but you can say that `A has a B`
composition is preferable.
For example a door **is not a** lock but it usually has one and it is usually interchangeable.
Therefore we can say that a door **has a** lock and that is why we would introduce a `lock` attribute
on the `Door` class.

Sometimes the case is not as clear-cut as the examples above so as always, use your judgement.

In our example we're going to demonstrate both using the door and lock metaphors.
Let's start with implementing the `open` story of the `Door` object.

# Overriding stories

```pycon

>>> from stories import arguments, story, Success

>>> class Door(object):
...     def __init__(self):
...         self.open = False
...
...     @story
...     @arguments("key")
...     def open(I):
...         I.set_open
...
...     def set_open(self, ctx):
...         self.open = True
...         return Success()

>>> class Lock(object):
...     def __init__(self):
...         self.locked = True
...
...     @story
...     @arguments("key")
...     def unlock(I):
...         I.set_unlocked
...
...     def set_unlocked(self, ctx):
...         self.locked = False
...         return Success()

```

If we wanted to implement a lockable door, we'd compose the lock over the door like so:

```pycon

>>> class LockableDoor(Door):
...     def __init__(self, lock):
...         self.unlock = lock.unlock
...
...     @story
...     @arguments("key")
...     def open(I):
...         I.unlock
...         I.set_open

```

We've overridden the `open` story to extend its behaviour.
So far, nothing new and everything works as expected.

## Super stories

As you may notice, we did copy the `set_open` step. If we were to have a door which requires multiple
steps we might have to do a lot of copy/pasting whenever we inherit.
However, calling `super(LockableDoor, self).open()` is simply not possible since we do not have a `self`
argument. This is because `open` is not an instance method or a class method.

But what if we we're to try to use the `@classmethod` decorator?

```pycon

>>> class LockableDoor(Door):
...     def __init__(self, lock):
...         self.unlock = lock.unlock
...
...     @story
...     @arguments("key")
...     @classmethod
...     def open(cls, I):
...         I.unlock
...         super(LockableDoor, cls).open(I)
Traceback (most recent call last):
  ...
_stories.exceptions.StoryDefinitionError: Story cannot be a class method.
<BLANKLINE>
Use @class_story instead:
@class_story
@arguments("key")
def open(cls, I):
    I.unlock
    super(LockableDoor, cls).open(I)
```

As you can understand from the exception message, if you want to call `super()` you need to use
the `@class_story` decorator instead of the regular `@story` decorator.

If you changed the code accordingly you should be seeing this:

```pycon
>>> from stories import class_story

>>> class LockableDoor(Door):
...     def __init__(self, lock):
...         self.unlock = lock.unlock
...
...     @class_story
...     @arguments("key")
...     def open(cls, I):
...         I.unlock
...         super(LockableDoor, cls).open(I)

>>> LockableDoor.open
LockableDoor.open
  unlock ??
  open (super story from Door)
    set_open

```

# Configurable stories

Sometimes we need more flexibility when creating our stories.
Since stories are simply Python code you can use branches to determine
which steps to execute.

```pycon
>>> from stories import arguments, class_story, story, Failure, Success

>>> class Lock(object):
...     def __init__(self):
...         self.locked = True
...
...     @story
...     @arguments("key")
...     def unlock(I):
...         I.set_unlocked
...
...     def set_unlocked(self, ctx):
...         self.locked = False
...         return Success()

>>> class KeycodeLock(Lock):
...     min_key_length = None
...     max_key_length = None
...     hasher = None
...
...     def __init__(self, secret_key):
...         self._secret_key = self.hash_key(key=secret_key)
...
...     @class_story
...     @arguments("key")
...     def unlock(cls, I):
...         if cls.min_key_length:
...             I.validate_key_min_length
...
...         if cls.max_key_length:
...             I.validate_key_max_length
...
...         if cls.hasher:
...             I.hash_key
...
...         I.authenticate
...
...         super(KeycodeLock, cls).unlock(I)
...
...     def validate_key_min_length(self, ctx):
...         return Success() if ctx.key > type(self).min_key_length else Failure()
...
...     def validate_key_max_length(self, ctx):
...         return Success() if ctx.key < type(self).max_key_length else Failure()
...
...     def authenticate(self, ctx):
...         return Success() if ctx.key == self._secret_key else Failure()
...
...     @class_story
...     @arguments("key")
...     def hash_key(cls, I):
...         I.create_hasher
...         I.hash
...
...     def create_hasher(self, ctx):
...         ctx.hasher = type(self).hasher(ctx.key)
...
...     def hash(self, ctx):
...         ctx.key = ctx.hasher.digest()
...         return Success()

>>> import hashlib

>>> class SecureKeycodeLock(KeycodeLock):
...     min_key_length = 16
...     hasher = hashlib.sha3_512

>>> SecureKeycodeLock.unlock
SecureKeycodeLock.unlock
  validate_key_min_length
  hash_key
    create_hasher
    hash
  authenticate
  unlock (super story from Lock)
      set_unlocked
```

!!! danger "Using multiple inheritance while not overriding the method is not supported"

    This is a current limitation of the implementation as we wanted to avoid such complexities.

    ```pycon
    >>> from stories import arguments, class_story, Failure, Success

    >>> class A(object):
    ...     @class_story
    ...     def example(cls, I):
    ...         I.one

    >>> class B(A):
    ...     @class_story
    ...     def example(cls, I):
    ...         I.two
    ...         super(B, cls).example(I)

    >>> class Mixin: pass

    >>> class C(Mixin, B):
    ...     pass

    >>> C.example
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Multiple inheritance not supported when method example not overridden in C
    ```
