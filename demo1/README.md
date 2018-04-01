# Demo 1

This demo has two objectives:

- Demonstrate using middleware to calculate metrics
- Demonstrate metric calculation, reporting and analysis

## Using middleware to calculate metrics

Depending on your underlying application framework, the mechanism of executing some code *before* a request is processed
and *after* a request is processed will different. Usually, such code is often executed as *middleware*. The Flask framework
supplies two decorator functions for this purpose:

- [before_request](http://flask.pocoo.org/docs/0.12/api/#flask.Flask.before_request) allows executing code before a request
  is processed
- [after_request](http://flask.pocoo.org/docs/0.12/api/#flask.Flask.after_request) allows executing code after a request is
  processed (but before a response is returned)

The [src](./src) sub-directory contains the application code. The main application is defined in [app.py](./src/app.py) with
the middleware functions defined in [helpers/middleware.py](./src/helpers/middleware.py). 

### Key snippets from `app.py`

The `setup_metrics()` function defined in the `middleware.py` file is called with the `app` instance we created for our
application to register the appropriates function to be called:

```
from helpers.middleware import setup_metrics
..
app = Flask(__name__)
setup_metrics(app)
..
```

As far as our metrics reporting is concerned, that's the only change we do to our application.

### Key snippets from `middleware.py`

THe `setup_metrics()` function which is called by our application above is defined in this module 
which has the following relevant code:

```
from flask import request
import time


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    # convert this into milliseconds for statsd
    resp_time = (time.time() - request.start_time)*1000
    ...
    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(stop_timer)
 ```

Using the `before_request()` function, the `start_timer()` function i


## Run demo

- Install `docker` and `docker-compose`
- `$ sudo docker-compose up`

## Play with the data

`docker-compose` run will print a URL which you can copy-paste into the browser on
our host.

Then, open the `Analysis` Jupyter Notebook by navigating to the `demo1` directory.
