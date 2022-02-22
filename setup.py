import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    sys.exit("Sorry, Python < 3.8 is not supported")


setup(
    name="workbench",
    version="1.1.0",
    author="Viacheslav Kovalevskyi",
    author_email="viacheslav@kovalevskyi.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "workbench=workbench.cli:main"
        ]
    },
    url="http://pypi.python.org/pypi/nmp/",
    license="LICENSE",
    description="GCP Vertex AI high level SDK",
    install_requires=[
        "docker==5.0.*",
        "google-cloud-aiplatform==1.1.*",
        "grpcio==1.36.*",
        "PyYAML==5.4.*"
    ],
    include_package_data=True,
    package_data={"workbench": ["workbench/prediction/container/Dockerfile", "workbench/prediction/container/requirements.txt"]},
)
