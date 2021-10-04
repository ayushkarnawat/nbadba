from distutils.core import setup
from setuptools import find_packages

setup(
    author="Rahul Pokharna, Sibi Sengottuvel, and Ayush Karnawat",
    author_email="rkp43@case.edu, ayush.karnawat97@gmail.com",
    description="NBA statistics dashboard",
    license="MIT",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    name="nbadba",
    packages=find_packages(),
    version="0.1.0",
)

