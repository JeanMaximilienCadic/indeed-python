from setuptools import setup
from indeed import __version__

setup(
    name="indeed",
    version=__version__,
    short_description="indeed",
    long_description="indeed",
    packages=[
        "indeed",
        "indeed.core",
        "indeed.etl",
        "indeed.tests",
        "indeed.models",
    ],
    include_package_data=True,
    package_data={'': ['*.yml']},
    license='MIT',
    python_requires='>=3.9',
    install_requires=[r.rsplit()[0] for r in open("requirements.txt")],
    description='indeed',
    platforms="linux_debian_10_x86_64",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
