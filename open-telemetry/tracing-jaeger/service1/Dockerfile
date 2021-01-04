FROM python:3.9
ADD . /application
WORKDIR /application
RUN pip install -r requirements.txt
CMD ["uwsgi", "--http", ":5000",  "--mount", "/myapplication=app:app", "--enable-threads", "--processes", "5"]