# syntax=docker/dockerfile:1

FROM kuralabs/python3-dev
WORKDIR /usr/src/RockNBlockTestTask
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
