import re

import setuptools

with open("README.md") as fp:
    long_description = fp.read()

requirements = ["kurigram>=2.0.69"]

# pyright: reportOptionalSubscript=false
with open(r"patchpyro\__init__.py") as fp:
    contents = fp.read()
    version = re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents)[1]


setuptools.setup(
    name="patchpyro",
    version=version,
    author="Cezar H. & adityaprasad502",
    author_email="plutoniumx502@gmail.com",
    license="LGPLv3+",
    description="A modified pyromod by a.devh.in",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adityaprasad502/patchpyro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "kurigram>=2.0.69",
    ],
)
