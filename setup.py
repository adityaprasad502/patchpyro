import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

with open("requirements.txt") as fp:
    requirements = [line.strip() for line in fp]

with open("pyropatch/__init__.py") as fp:
    version = "2.0.0"


setuptools.setup(
    name="pyropatch",
    version=version,
    author="Cezar H. & adityaprasad502",
    license="LGPLv3+",
    description="A modified pyromod by www.da.gd/aditya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adityaprasad502/pyropatch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
)
