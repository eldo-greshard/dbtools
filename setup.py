from setuptools import setup, find_packages

setup(
    name="dbtools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
        "sentence-transformers",
        "scipy",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "dbtools=dbtools.cli:main",
        ],
    },
    author="Eldo Greshard",
    description="Database comparison and data restoration tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux Server",
    ],
)
