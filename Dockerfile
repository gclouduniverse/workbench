FROM python:3.10

COPY ./. /app/
RUN python3 -m pip install --upgrade build
RUN cd /app/ && python3 -m pip install --upgrade build
RUN pip install /app/.
# just for testing
# RUN workbench --version

ENTRYPOINT ["workbench"]