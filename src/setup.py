from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "../README.md")

with open(readme_path, "r") as f:
    description = f.read()

print(description)

setup(
    name='bdomarket',
    version='0.1.2',
    author="Szőke Dominik",
    packages=find_packages(),
    install_reqires=[
        "requests>=2.25.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/Fizzor96/bdomarket",
    long_description=description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8"
)