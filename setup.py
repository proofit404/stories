from setuptools import setup


readme = open("README.rst").read() + open("CHANGELOG.rst").read()


setup(
    name="stories",
    version="0.9",
    description="Define a user story in the business transaction DSL",
    long_description=readme,
    license="BSD",
    url="https://github.com/proofit404/stories",
    author="Artem Malyshev",
    author_email="proofit404@gmail.com",
    package_dir={"": "src"},
    packages=[
        "stories",
        "stories._exec",
        "stories.contrib",
        "stories.contrib.debug_toolbars",
        "stories.contrib.debug_toolbars.django",
        "stories.contrib.sentry",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={"pytest11": ["stories = stories.contrib.pytest"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
    ],
)
