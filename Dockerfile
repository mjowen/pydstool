# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.8.0
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files. (Doing this breaks pydstool so we don't want that)
#ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

RUN apt-get update && apt-get install -qq gfortran swig

RUN apt-get install git -y

RUN apt-get install nano

COPY . .

RUN python setup.py develop

#WORKDIR /app/examples

#Uncomment the following line to run tests on container start-up
#CMD python run_all_tests.py
