FROM python:3.7.4
ADD . /take-home
WORKDIR /take-home
RUN pip3 install -r requirements.txt
RUN cd /tmp && python3 /take-home/downloader.py 1QLBGFOoKw_3-iM58q4unWfwHmPqfnrYr chicago_taxi_trips_2020.parquet