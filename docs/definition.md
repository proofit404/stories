# Definition

Technically speaking, a story is a method of the class which calls
other methods of this class in special order.

The body of the story isn't executed directly. It's used as a spec of
what should happen. The main purpose of it is to describe the intent.

The steps of the story could be either regular methods or
coroutines. This could not be mixed. All methods of the story should
be of one type. If steps of the story are coroutines, you can await
the story itself.

## Basics

This is a real-world example of the story definition used in our
[tutorials](https://github.com/dry-python/tutorials). As you can see,
it is a business process of the subscription to our service.

```pycon tab="sync"

>>> from stories import Failure, Result, Success, arguments, story

>>> class Subscription:
...     """Buy subscription for certain category."""
...
...     @story
...     @arguments("category_id", "price_id", "user_id")
...     def buy(I):
...
...         I.find_category
...         I.find_price
...         I.find_profile
...         I.check_balance
...         I.persist_payment
...         I.persist_subscription
...         I.send_subscription_notification
...         I.show_category
...
...     def find_category(self, ctx):
...
...         category = load_category(ctx.category_id)
...         return Success(category=category)
...
...     def find_price(self, ctx):
...
...         price = load_price(ctx.price_id)
...         return Success(price=price)
...
...     def find_profile(self, ctx):
...
...         profile = load_profile(ctx.user_id)
...         return Success(profile=profile)
...
...     def check_balance(self, ctx):
...
...         if ctx.profile.balance > ctx.price.cost:
...             return Success()
...         else:
...             return Failure()
...
...     def persist_payment(self, ctx):
...
...         decrease_balance(ctx.profile, ctx.price.cost)
...         save_profile(ctx.profile)
...         return Success()
...
...     def persist_subscription(self, ctx):
...
...         expires = calculate_period(ctx.price.period)
...         subscription = create_subscription(
...             ctx.profile, ctx.category, expires
...         )
...         return Success(subscription=subscription)
...
...     def send_subscription_notification(self, ctx):
...
...         notification = send_notification(
...             "subscription", ctx.profile, ctx.category.name
...         )
...         return Success(notification=notification)
...
...     def show_category(self, ctx):
...
...         return Result(ctx.category)

```

```pycon tab="async"

>>> from stories import Failure, Result, Success, arguments, story

>>> class Subscription:
...     """Buy subscription for certain category."""
...
...     @story
...     @arguments("category_id", "price_id", "user_id")
...     def buy(I):
...
...         I.find_category
...         I.find_price
...         I.find_profile
...         I.check_balance
...         I.persist_payment
...         I.persist_subscription
...         I.send_subscription_notification
...         I.show_category
...
...     async def find_category(self, ctx):
...
...         category = await load_category(ctx.category_id)
...         return Success(category=category)
...
...     async def find_price(self, ctx):
...
...         price = await load_price(ctx.price_id)
...         return Success(price=price)
...
...     async def find_profile(self, ctx):
...
...         profile = await load_profile(ctx.user_id)
...         return Success(profile=profile)
...
...     async def check_balance(self, ctx):
...
...         if ctx.profile.balance > ctx.price.cost:
...             return Success()
...         else:
...             return Failure()
...
...     async def persist_payment(self, ctx):
...
...         await decrease_balance(ctx.profile, ctx.price.cost)
...         await save_profile(ctx.profile)
...         return Success()
...
...     async def persist_subscription(self, ctx):
...
...         expires = await calculate_period(ctx.price.period)
...         subscription = await create_subscription(
...             ctx.profile, ctx.category, expires
...         )
...         return Success(subscription=subscription)
...
...     async def send_subscription_notification(self, ctx):
...
...         notification = await send_notification(
...             "subscription", ctx.profile, ctx.category.name
...         )
...         return Success(notification=notification)
...
...     async def show_category(self, ctx):
...
...         return Result(ctx.category)

```

### Explanation

There are a few terms you should be familiar with:

1. `@story` decorated method represents the spec of the business
   process. It's executed only once at the class definition
   moment. This class attribute became a smart business object.
2. `@arguments` decorator describes input data similar to function
   arguments.
3. `I` object is used to build the execution spec out of its
   attributes. You can use any **human-readable** names.
4. Methods defined in the class are story steps. They will be called
   by the smart business object defined with the `@story`
   decorator. Usually, they just delegate responsibility to the call
   of other function with proper variables from the context.
5. `self` in step methods is the real instance of the `Subscription`
   class. You own this class. It's up to you how to write it. The
   smart business object will use its instance to resolve its steps.
6. `ctx` is a scope of variables available to step methods. Context is
   initiated from input data passed to the business object. It can be
   extended by previously executed step methods with keyword arguments
   to the `Success()` marker.
7. `Success`, `Failure` and `Result` are markers returned by step
   methods to change business process execution path.

### Invalid story definitions

Some story definitions are invalid.
If such a story is defined it may raise an error whenever the `@story` decorator wraps
the story definition method or whenever you run it, depending on the invalid story in question.

#### Story definitions which return a coroutine

!!! danger "The story definition method itself must not be declared with `async def`"

    Attempting to do so will raise a `StoryDefinitionError`.

    ```pycon tab="sync"

    >>> from stories import Success, story

    >>> class InvalidStoryDefinition:
    ...     """An example of an invalid story that is defined using `async def`."""
    ...
    ...     @story
    ...     async def example(I):
    ...
    ...         I.step
    ...
    ...     def step(self, ctx):
    ...
    ...         return Success()
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Story should be a regular function

    ```

    ```pycon tab="async"

    >>> from stories import Success, story

    >>> class InvalidStoryDefinition:
    ...     """An example of an invalid story that is defined using `async def`."""
    ...
    ...     @story
    ...     async def example(I):
    ...
    ...         I.step
    ...
    ...     async def step(self, ctx):
    ...
    ...         return Success()
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Story should be a regular function

    ```

##### Explanation

1. Building a story is a synchronous operation.
2. If a story definition method were to return a coroutine, it would leak since since it
   is never `await`ed.

#### Empty Stories

!!! danger "Story definitions without any steps are invalid"

    Attempting to define such a story will raise a `StoryDefinitionError`.

    ```pycon

    >>> from stories import story

    >>> class EmptyStory:
    ...     """An example of an empty story."""
    ...
    ...     @story
    ...     def empty(I):
    ...
    ...         pass
    Traceback (most recent call last):
       ...
    _stories.exceptions.StoryDefinitionError: Story should have at least one step defined

    ```

##### Explanation

1. Stories without any steps are meaningless.
   Their result is unclear and they serve no purpose.
2. We require you to define at least one step to determine whether the story
   is synchronous or asynchronous.

#### Mixing synchronous steps and asynchronous steps

!!! danger "All steps must either be synchronous or asynchronous"

    Attempting to access a story with synchronous steps or sub-stories which contain
    such steps will raise a `StoryDefinitionError`.

    ```pycon tab="sync"

    >>> from stories import Success, story

    >>> class MixedStory:
    ...     """An example of an invalid synchrnous story that incorporates an asynchronous step."""
    ...
    ...     @story
    ...     def example(I):
    ...
    ...         I.synchronous_step
    ...         I.asynchronous_step
    ...
    ...     def synchronous_step(self, ctx):
    ...
    ...         return Success()
    ...
    ...     async def asynchronous_step(self, ctx):
    ...
    ...         return Success()
    >>> MixedStory().example
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Coroutines and functions can not be used together in story definition.
    <BLANKLINE>
    This method should be a function: MixedStory.asynchronous_step
    <BLANKLINE>
    Story method: MixedStory.example

    ```

    ```pycon tab="async"

    >>> from stories import Success, story

    >>> class MixedStory:
    ...     """An example of an invalid asynchrnous story that incorporates an synchronous step."""
    ...
    ...     @story
    ...     def example(I):
    ...
    ...         I.asynchronous_step
    ...         I.synchronous_step
    ...
    ...     async def asynchronous_step(self, ctx):
    ...
    ...         return Success()
    ...
    ...     def synchronous_step(self, ctx):
    ...
    ...         return Success()
    >>> MixedStory().example
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Coroutines and functions can not be used together in story definition.
    <BLANKLINE>
    This method should be a coroutine: MixedStory.synchronous_step
    <BLANKLINE>
    Story method: MixedStory.example

    ```

    Likewise, injecting a synchronous sub-story to an asynchronous story
    or the contrary is also forbidden.

    ```pycon tab="sync"

    >>> from stories import Success, story

    >>> class MixedStory:
    ...     """An example of an invalid synchrnous story that incorporates an asynchronous sub-story."""
    ...
    ...     @story
    ...     def example(I):
    ...
    ...         I.synchronous_step
    ...         I.asynchronous_substory
    ...
    ...     @story
    ...     def asynchronous_substory(I):
    ...
    ...         I.asynchronous_step
    ...
    ...     def synchronous_step(self, ctx):
    ...
    ...         return Success()
    ...
    ...     async def asynchronous_step(self, ctx):
    ...
    ...         return Success()
    >>> MixedStory().example
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Coroutine and function stories can not be injected into each other.
    <BLANKLINE>
    Story function method: MixedStory.example
    <BLANKLINE>
    Substory coroutine method: MixedStory.asynchronous_substory

    ```

    ```pycon tab="async"

    >>> from stories import Success, story

    >>> class MixedStory:
    ...     """An example of an invalid synchrnous story that incorporates an asynchronous sub-story."""
    ...
    ...     @story
    ...     def example(I):
    ...
    ...         I.asynchronous_step
    ...         I.synchronous_substory
    ...
    ...     @story
    ...     def synchronous_substory(I):
    ...
    ...         I.synchronous_step
    ...
    ...     async def asynchronous_step(self, ctx):
    ...
    ...         return Success()
    ...
    ...     def synchronous_step(self, ctx):
    ...
    ...         return Success()
    >>> MixedStory().example
    Traceback (most recent call last):
      ...
    _stories.exceptions.StoryDefinitionError: Coroutine and function stories can not be injected into each other.
    <BLANKLINE>
    Story coroutine method: MixedStory.example
    <BLANKLINE>
    Substory function method: MixedStory.synchronous_substory

    ```

##### Explanation

1. Running a synchronous step or sub-story in an asynchronous story may block the event loop.
   If the event loop is blocked for too long the program's performance might suffer.
2. Running a asynchronous step or sub-story in an synchronous story will cause an error
   since the step returns a coroutine which is not one of the accepted return types for a step
   or a sub-story.
   In addition it will cause a coroutine leak since we don't `await` it.

!!! note

    This is a limitation that will be lifted by a future version.

    When defining an asynchronous story, we will require you to explictly specify
    that the synchronous step or sub-story will execute in a worker thread.

    Likewise, when defining a synchronous story, we will require you to explictly specify
    that the asynchronous step or sub-story will execute in an event loop.

## Failure protocols

To make failure handling a more manageable process we can define a
[failure protocol](failure_protocol.md).

```pycon tab="sync"

>>> from enum import Enum, auto
>>> from stories import Failure, Result, Success, arguments, story

>>> class ShowCategory:
...     """Show category entries."""
...
...     @story
...     @arguments("category_id", "user_id")
...     def show(I):
...
...         I.find_subscription
...         I.check_expiration
...         I.find_category
...         I.show_category
...
...     def find_subscription(self, ctx):
...
...         subscription = load_subscription(ctx.category_id, ctx.user_id)
...         if subscription:
...             return Success(subscription=subscription)
...         else:
...             return Failure(Errors.forbidden)
...
...     def check_expiration(self, ctx):
...
...         if ctx.subscription.is_expired():
...             return Failure(Errors.forbidden)
...         else:
...             return Success()
...
...     def find_category(self, ctx):
...
...         category = load_category(ctx.category_id)
...         if category:
...             return Success(category=category)
...         else:
...             return Failure(Errors.not_found)
...
...     def show_category(self, ctx):
...
...         return Result(ctx.category)

>>> @ShowCategory.show.failures
... class Errors(Enum):
...
...     forbidden = auto()
...     not_found = auto()

```

```pycon tab="async"

>>> from enum import Enum, auto
>>> from stories import Failure, Result, Success, arguments, story

>>> class ShowCategory:
...     """Show category entries."""
...
...     @story
...     @arguments("category_id", "user_id")
...     def show(I):
...
...         I.find_subscription
...         I.check_expiration
...         I.find_category
...         I.show_category
...
...     async def find_subscription(self, ctx):
...
...         subscription = await load_subscription(ctx.category_id, ctx.user_id)
...         if subscription:
...             return Success(subscription=subscription)
...         else:
...             return Failure(Errors.forbidden)
...
...     async def check_expiration(self, ctx):
...
...         if await ctx.subscription.is_expired():
...             return Failure(Errors.forbidden)
...         else:
...             return Success()
...
...     async def find_category(self, ctx):
...
...         category = await load_category(ctx.category_id)
...         if category:
...             return Success(category=category)
...         else:
...             return Failure(Errors.not_found)
...
...     async def show_category(self, ctx):
...
...         return Result(ctx.category)

>>> @ShowCategory.show.failures
... class Errors(Enum):
...
...     forbidden = auto()
...     not_found = auto()

```

### Explanation

1. `Failure` marker takes optional `reason` argument. It can be used
   in the caller code to handle this failure. For example, to show a
   proper error code to the user.
2. Failure protocol should be defined after the story to allow passing
   `reason` in the `Failure` marker.
