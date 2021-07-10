import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    sys.exit("Sorry, Python < 3.8 is not supported")

setup(
    name="vaip",
    version="1",
    author="Viacheslav Kovalevskyi",
    author_email="viacheslav@kovalevskyi.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "vaip=vaip.cli:main"
        ]
    },
    url="http://pypi.python.org/pypi/nmp/",
    license="LICENSE",
    description="GCP Vertex AI Prediction high level SDK",
    install_requires=open("requirements.txt").read().split("\n"),
    include_package_data=True,
    package_data={"vaip": ["vaip/container/Dockerfile", "vaip/container/Dockerfile"]},
)
