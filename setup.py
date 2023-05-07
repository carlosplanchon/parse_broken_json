#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="parse_broken_json",
    packages=find_packages(),
    version="0.1",
    license="MIT",
    description="Library to help parsing broken and invalid JSON.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos Andrés Planchón Prestes",
    author_email="carlosandresplanchonprestes@gmail.com",
    url="https://github.com/carlosplanchon/parse_broken_json",
    keywords=["parsing", "broken", "json", "invalid"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        "ijson",
    ]
)
