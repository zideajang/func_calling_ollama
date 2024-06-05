from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here,"README.md"),encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='function_calling_ollama',
    version='1.0.0',
    author='zidea',
    author_email='zidea2015@163.com',
    description='function calling ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="func calling for local models supported by ollama",
    url="https://github.com/zideajang/func_calling_ollama",
    # install_requires=requirements,
    packages=find_packages(exclude=["examples","docs"]),
    python_requires=">=3.9"
)