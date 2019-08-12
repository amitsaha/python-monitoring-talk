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

RUN chmod +x /application/start.sh
CMD ["/application/start.sh"]
