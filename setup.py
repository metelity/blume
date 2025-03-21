from setuptools import setup, find_packages

setup(
    name="blume",
    version="1.0.0",
    author="metelity",
    description="A database management library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/metelity/blume",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "blume=blume.cli:main", 
        ],
    },
)
