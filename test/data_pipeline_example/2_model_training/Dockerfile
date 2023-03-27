#FROM frolvlad/alpine-python-machinelearning
FROM --platform=linux/amd64 python:3.8
#FROM --platform=linux/amd64  pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "training_model.py"]
