FROM python:3.11-slim

# set working directory
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# install python dependencies
COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-dependencies

# add app
COPY . .
