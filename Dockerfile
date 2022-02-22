FROM 3.10-bullseye

RUN pip install .
# just for testing
RUN workbench --version

ENTRYPOINT ["workbench"]