"""Setup configuration for res_match_crawler."""

from setuptools import setup, find_packages

setup(
    name="res_match_crawler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "lxml>=4.9.3",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0"],
    },
    python_requires=">=3.8",
)
