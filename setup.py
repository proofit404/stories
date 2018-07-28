from setuptools import setup


setup(
    name="stories",
    version="0.8",
    description="Define a user story in the business transaction DSL",
    url="https://github.com/proofit404/stories",
    license="BSD",
    author="Artem Malyshev",
    author_email="proofit404@gmail.com",
    packages=["stories", "stories._exec", "stories.contrib"],
    entry_points={"pytest11": ["stories = stories.contrib.pytest"]},
)
