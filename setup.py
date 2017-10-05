from setuptools import setup, find_packages


setup(
    name='pydplace',
    version='0.4',
    license='CC-BY-4.0',
    description='programmatic access to D-PLACE/dplace-data',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    author='Robert Forkel',
    author_email='forkel@shh.mpg.de',
    url='https://d-place.shh.mpg.de',
    keywords='data',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clldutils>=1.9',
        'attrs',
        'pyglottolog>=0.3.2',
        'python-nexus>=1.4.2',
        'pycldf>=1.0',
        'ete3>=3.0.0b34',
    ],
    entry_points={
        'console_scripts': [
            'dplace=pydplace.cli:main',
        ]
    },
    tests_require=[],
    test_suite="pydplace"
)
