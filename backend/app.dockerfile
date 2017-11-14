FROM python:2.7
MAINTAINER Ruhan "mobbyd1@gmail.com"
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD /backend/app /usr/src/app
RUN pip install flask
RUN pip install redis
CMD python url_shortener.py
EXPOSE 5000
