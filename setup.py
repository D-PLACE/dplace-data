from setuptools import setup, find_packages


setup(
    name='pydplace',
    version='0.1',
    description='programmatic access to D-PLACE/dplace-data',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    author='',
    author_email='forkel@shh.mpg.de',
    url='',
    keywords='data',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clldutils>=1.9',
        'attrs',
        'fiona',
        'shapely',
        'pyglottolog>=0.3.2',
    ],
    entry_points={
        'console_scripts': [
            'dplace=pydplace.cli:main',
        ]
    },
    tests_require=[],
    test_suite="pydplace")
