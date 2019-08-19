import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marklogic_client",
    version="0.0.1",
    author="Han Kruiger",
    description="A class for talking with MarkLogic Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quangis/marklogic_client",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests >= 2.22.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'python-dotenv',
    ],
)
