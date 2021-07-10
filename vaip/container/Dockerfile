FROM gcr.io/deeplearning-platform-release/base-cpu

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install Flask==1.1.*
COPY ./* ./
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
