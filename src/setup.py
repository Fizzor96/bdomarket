from setuptools import setup, find_packages
import os

# here = os.path.abspath(os.path.dirname(__file__))
# readme_path = os.path.join(here, "..\\README.md")

# with open(readme_path, "r") as f:
#     description = f.read()

setup(
    name='bdomarket',
    version='0.1.7',
    author="Szőke Dominik",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.13.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Fizzor96/bdomarket",
    # long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8"
)