from setuptools import setup, find_packages
import eckity

VERSION = eckity.__version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='eckity',
    version=VERSION,
    author='Moshe Sipper, Achiya Elyasaf, Itai Tzruia, Tomer Halperin',
    author_email='sipper@gmail.com, achiya@bgu.ac.il, itaitz@post.bgu.ac.il, tomerhal@post.bgu.ac.il',
    description='EC-KitY: Evolutionary Computation Tool Kit in Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://www.eckity.org',
    project_urls={
        "Bug Tracker": "https://github.com/EC-KitY/EC-KitY/issues"
    },
    license='GNU GPLv3',
    packages=find_packages(),
    install_requires=["numpy>=1.23.0", "overrides>=7.0.0", "pandas>=0.25.2"],
)
