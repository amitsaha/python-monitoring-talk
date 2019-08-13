# Example Django application

See `src` for the application code and top level README for the description of this repo from a functionality
point of view. This demo shows how we can use the statsd exporter to monitor a Django application using
prometheus.


## Building Docker image

The Python 3 based [Dockerfile](Dockerfile) uses an Alpine Linux base image
and copies the source code to the image:

```
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

```

The `/start.sh` script runs the Django DB migrations and then uses `gunicorn` to run our
application using 5 worker processes.

To build the image:

```
$ docker build -t amitsaha/til:statsd-prometheus .
```

## Running the application

We can just run the web application as follows:

```
$ docker run  -ti -p 8000:8000 amitsaha/til:statsd-prometheus
```

## Bringing up the web application, along with prometheus

The [docker-compse.yml](docker-compose.yml) brings up the `webapp.example.com` service which is our web application
using the image `amitsaha/til:prometheus` we built above. The [docker-compose-infra.yml](docker-compose-infra.yml)
file brings up `prometheus` service, `statsd` service (running the statsd exporter) and also starts the `grafana` service which
is available on port 3000. The config directory contains a `prometheus.yml` file
which sets up the targets for prometheus to scrape. The scrape configuration 
looks as follows:

```
# my global config
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # By default, scrape targets every 15 seconds.
  # scrape_timeout is set to the global default (10s).

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
      monitor: 'my-project'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
         - targets: ['localhost:9090']
  - job_name: 'webapp'
    scrape_interval: 5s
    static_configs:
        - targets: ['statsd:9102']


```

Prometheus scrapes itself, which is the first target above. The second target
is the statsd exporter.

Since these services are running via `docker-compose`, `webapp.example.com` automatically resolves to the IP of the django web application.

To bring up all the services:

```
$ docker-compose build
$ docker-compose -f docker-compose.yml -f docker-compose-infra.yml up
```

Then, create the following `/etc/hosts/` entry:

```
127.0.0.1 webapp.example.com
```

Now, in your browser visit, `http://webapp.example.com:8080` and you should see the web application.

Go to `http://127.0.0.1:3000` to access the Grafana instance and login with `admin` as username and 
`foobar` as password.
