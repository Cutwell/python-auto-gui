# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='Python Pyre',

    version='1.0.0',

    description='Instantly generate GUI functionality for any Python program using Python-Pyre.',

    # The project's main homepage.
    url='https://github.com/cutwell/Python-Pyre',

    # Author details
    author='Zachary Smith',
    author_email='zachsmith.dev@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Stable',

        'Intended Audience :: Developers',

        'License :: MIT License',

        'Programming Language :: Python :: 3',
    ],

    keywords='automated gui generation',

    py_modules=["pyre.py"],
)
