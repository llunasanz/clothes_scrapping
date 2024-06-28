FROM python:3.10

RUN mkdir /srv/project/

# RUN mkdir /srv/project/scrapper

# RUN mkdir /srv/project/schema

# RUN mkdir /srv/project/src

# RUN mkdir /srv/project/src/test

COPY assets /srv/project/assets

COPY scrapper /srv/project/scrapper

COPY schema /srv/project/schema

COPY requirements.txt /srv/project/requirements.txt

COPY src /srv/project/src

COPY tests /srv/project/tests

WORKDIR /srv/project/

RUN mkdir output/

RUN pip3 install -r requirements.txt

EXPOSE 34617
