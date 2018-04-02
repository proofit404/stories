from unittest import TestCase, main

from stories import Failure, Result, Success, argument, story


class My:

    @story
    @argument("a")
    @argument("b")
    def x(self):
        self.one()
        self.two()
        self.three()

    def one(self):

        return Success()

    def two(self):

        if self.input.a > 1:
            return Failure()

        return Success(c=4)

    def three(self):

        return Result(self.input.b - self.input.c)


class StoryTest(TestCase):

    def test_failure(self):

        result = My().x(2, 2)
        self.assertIsInstance(result, Failure)

    def test_success(self):

        result = My().x(1, 2)
        self.assertEqual(result, -2)

    def test_success_keywords(self):

        result = My().x(a=1, b=2)
        self.assertEqual(result, -2)

    def test_assertion_error(self):

        with self.assertRaises(AssertionError):
            My().x(1)

    def test_assertion_error_keywords(self):

        with self.assertRaises(AssertionError):
            My().x(1, b=2)


# TODO: test My().y() without arguments at all.

if __name__ == "__main__":
    main()
