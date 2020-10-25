import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phpypam",
    version="0.1.2",
    author="Christian Meißner",
    author_email="Christian Meißner <cme+codeaffen@meissner.sh>",
    description="Python API client library for phpIPAM installation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    platform="Independent",
    url="https://codeaffen.github.io/phpypam",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
    keywords='api phpipam',
    python_requires='>=3.6',
    install_requires=[
        'requests (>=2.21,<3.0)',
    ],
)
