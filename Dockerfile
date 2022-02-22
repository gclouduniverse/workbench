FROM python:3.10

COPY workbench /app/workbench/
COPY requirements.txt /app/requirements.txt
COPY setup.py /app/setup.py
COPY MANIFEST.in /app/MANIFEST.in
COPY LICENSE /app/LICENSE
RUN pip install /app/.

ENTRYPOINT ["workbench"]