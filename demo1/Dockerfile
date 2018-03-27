FROM python:3.6.1-alpine
ADD . /application
WORKDIR /application
RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
        apache2-utils \
	; \
	pip install -r src/requirements.txt; \
	apk del .build-deps;
EXPOSE 5000
WORKDIR /application
CMD ["python", "app.py"]
