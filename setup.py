import re
from os.path import join, dirname
from setuptools import setup, find_packages

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'image-utility', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'tkinter',
    'opencv-python',
]


setup(
    name="image utility",
    version=package_version,
    author="Sepideh Shamsizadeh",
    author_email="sepideh@carrene.com",
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'image-utility = image-utility.cli:main'
        ]
    },
    packages=find_packages(),
)