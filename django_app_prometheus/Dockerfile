FROM python:3.7-alpine
ADD src /application
WORKDIR /application
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	; \
	pip install -r requirements.txt; \
	apk del .build-deps;
EXPOSE 8000
VOLUME /application

CMD gunicorn --workers 5 --bind 0.0.0.0:8000  til.wsgi
