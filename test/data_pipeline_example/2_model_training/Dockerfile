#FROM frolvlad/alpine-python-machinelearning
FROM --platform=linux/amd64 python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "training_model.py"]
