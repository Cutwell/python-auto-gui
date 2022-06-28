import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pythonautogui',
    author='Zachary Smith',
    author_email='zachsmith.dev@gmail.com',
    description='Generate a Tkinter GUI from any Python program',
    keywords='tkinter, gui, gui-automation, gui-automation-python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Cutwell/python-auto-gui',
    project_urls={
        'Documentation': 'https://github.com/Cutwell/python-auto-gui',
        'Bug Reports':
        'https://github.com/Cutwell/python-auto-gui/issues',
        'Source Code': 'https://github.com/Cutwell/python-auto-gui',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',

        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['Pillow'],
    extras_require={
        #'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)