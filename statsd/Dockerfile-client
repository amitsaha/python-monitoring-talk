FROM python:3.6.1-alpine
RUN apk add --update curl apache2-utils && rm -rf /var/cache/apk/*
ADD ./make-requests.sh /make-requests.sh
VOLUME /data
CMD ["/bin/sh", "/make-requests.sh"]
