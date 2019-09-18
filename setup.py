import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sanic_gzip",
    version="0.2.0",
    author="Damien Alexandre",
    author_email="damien.alexandre@muage.org",
    description="Add compress to Sanic response as decorator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koug44/sanic-gzip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
