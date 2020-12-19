from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

requires = [
    "pandas>=0.21",
    "importlib_metadata>=0.7; python_version < '3.8'",
]

setup(
    name="forceatlas2-python",
    use_scm_version=True,
    description="scRNA-Seq analysis tools that scale to millions of cells",
    long_description=long_description,
    url="https://github.com/klarman-cell-observatory/forceatlas2-python",
    author="Joshua Gould, Yiming Yang, Bo Li",
    author_email="cumulus-support@googlegroups.com",
    classifiers=[  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="Force Directed Layout",
    packages=find_packages(),
    install_requires=requires,
    setup_requires=['setuptools_scm'],
    python_requires="~=3.5",
    package_data={
        "forceatlas2": ["ext/forceatlas2.jar", "ext/gephi-toolkit-0.9.2-all.jar"]
    }
)
