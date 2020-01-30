import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="uni2ascii-janin",
    version="1.1.0",
    author="Adam Janin",
    author_email="pypi@janin.org",
    description="Convert unicode characters that resemble ASCII to their equivalent.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajanin/uni2ascii",
    packages=setuptools.find_packages(),
    scripts=['scripts/uni2ascii'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
