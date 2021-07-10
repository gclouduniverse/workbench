FROM gcr.io/deeplearning-platform-release/tf2-gpu

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY requirements-flask.txt requirements-flask.txt
RUN pip3 install -r requirements-flask.txt
COPY ./* ./
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
