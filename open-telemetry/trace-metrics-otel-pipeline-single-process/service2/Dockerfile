FROM python:3.9
RUN apt-get -y update && apt-get -y install libprotobuf17 python-pkg-resources python-protobuf python-six
RUN pip install mysql-connector

ADD . /application
WORKDIR /application
RUN pip install -r requirements.txt
CMD ["uwsgi", "--http", ":5000",  "--mount", "/myapplication=app:app", "--processes", "1"]
