FROM python:3.10

RUN mkdir /srv/project/

RUN mkdir /srv/project/scrapper

RUN mkdir /srv/project/schema

COPY scrapper/scrap.py /srv/project/scrapper/scrap.py

COPY schema/product.py /srv/project/schema/product.py

COPY requirements.txt /srv/project/requirements.txt

WORKDIR /srv/project/

RUN mkdir output/

RUN pip3 install -r requirements.txt

EXPOSE 34617
