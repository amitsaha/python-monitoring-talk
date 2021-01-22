FROM python:3.9
ADD . /application
WORKDIR /application
RUN pip install -r requirements.txt --use-deprecated=legacy-resolver
CMD ["uwsgi", "--http", ":5000",  "--mount", "/myapplication=app:app", "--processes", "1"]
