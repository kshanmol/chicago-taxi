FROM python:3.7.4
ADD . /take-home
WORKDIR /take-home
RUN pip3 install -r requirements.txt
RUN cd /tmp && wget -O chicago_taxi_trips_2020.parquet "https://www.dropbox.com/s/r71iostpglhrlwg/chicago_taxi_trips_2020.parquet?dl=0"
#RUN PYTHONPATH=$(pwd)/src/ pytest