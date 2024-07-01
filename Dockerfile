FROM python:3.10

RUN mkdir /srv/project/

COPY app /srv/project/app

COPY assets /srv/project/assets

COPY schema /srv/project/schema

COPY requirements.txt /srv/project/requirements.txt

COPY src /srv/project/src

COPY tests /srv/project/tests

WORKDIR /srv/project/

RUN mkdir output/

RUN pip3 install -r requirements.txt

EXPOSE 34617
