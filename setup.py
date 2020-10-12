import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhpipam",
    version="0.0.1",
    author="Christian Meißner",
    author_email="Christian Meißner <cme+codeaffen@meissner.sh>",
    description="Python API client library for phpIPAM installation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    platform="Independent",
    url="https://github.com/codeaffen/pyhpipam",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
