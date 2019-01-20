from setuptools import setup, find_packages

setup(
    name='swp2018',
    version='0.0.1a',
    description='CLI tool to parse PAGE XML files and convert them to TEI files.',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'lxml'
    ],
    url='https://github.com/thvitt/swp2018',
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)
