from setuptools import setup, find_packages

setup(
    name="vaip",
    version="1",
    author="Viacheslav Kovalevskyi",
    author_email="viacheslav@kovalevskyi.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "vaip = vaip.cli:main"
        ]
    },
    url="http://pypi.python.org/pypi/nmp/",
    license="LICENSE",
    description="GCP Vertex AI Prediction high level SDK",
    install_requires=open("requirements.txt").read().split("\n"),
)
