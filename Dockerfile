FROM python:3.7.4
ADD . /take-home
WORKDIR /take-home
RUN pip3 install -r requirements.txt