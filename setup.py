import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    sys.exit("Sorry, Python < 3.8 is not supported")


setup(
    name="ai-workbench",
    version="1.2.0",
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
        "PyYAML==5.4.*",
        "google-api-python-client==2.37.*",
        "six==1.16.*",
        "google-cloud-storage==1.32.*",
        "nbformat==5.1.*"
    ],
    include_package_data=True,
    package_data={"workbench": ["workbench/prediction/container/Dockerfile", "workbench/prediction/container/requirements.txt"]},
)
