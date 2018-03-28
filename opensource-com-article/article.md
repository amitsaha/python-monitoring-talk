## Introduction

My reaction when I first came across the terms `counter` and `gauge` and the graphite
dashboards with various colors with numbers labelled mean and upper 90 was one of avoidance.
It's like I saw them, but I didn't care about them - mostly because I didn't understand them
or hadn't read about what they may be useful for. My job role at that point of time didn't
require me to pay attention to them. Hence, they remained ignored. 

That was around 2 years back. Then my role organically
started changing - rather I started changing it proactively and then I reached a point where
I wanted to ask a lot of questions about our network applications and get answers to them.
And that is where, I started learning about `metrics`. Today's post (and soon to be my talk
at PyCon US 2018) is about what I have learned so far. 

The three stages that I have gone through so far in my personal monitoring journey can be said
to be:

- Stage 1: What? (Looks elsewhere)
- Stage 2: Without metrics we are really flying blind
- Stage 3: How not to do metrics wrong?

I am currently in _Stage 2_ and today I will be sharing what I have learned so far. Gradually,
I have also been trying to do some _Stage 3_ readings which I will share at the end.

Let's get started!

## Why should I monitor?

The top reasons for monitoring are:

- Understand _normal_ and _abnormal_ system and service behavior
- Capacity planning, scaling up or down
- Assist in performance troubleshooting
- Understand the effect of software/hardware changes
- Change system behavior in response to a measurement
- Alert when system exhibits unexpected behavior

## Metric and Metric types

Let's start with learning what is a __metric__.  A __metric__ for our purposes is a _observed_ value of a certain 
quantity at a given point of _time_. The total number hits on a blog post, the total number of people in a talk,
the number of times the data was not found in caching system, the number of logged-in users on your website are all 
examples of metrics. They broadly fall into these categories:

**Counter**

Consider your personal blog. You just posted your latest post and want to keep an eye
on how many hits your post since it was posted. The number of hits so far can only ever *increase*.
This is an example of a __counter__ metric. It's value starts at 0 and can only ever go up during the
lifetime of your blog post. Graphically, a counter looks like this:

![A Counter metric always increases][counter-graph.png]

**Gauge**

Instead of the total number of hits on your blog post, let's say we want to track the number of hits per day or 
per week. This is a metric whose value can go up or down and is referred to as a __gauge__.

Graphically, a gauge looks like this:


![A gauge metric can increase or decrease][gauge-graph.png]

The value of a __gauge__ would usually have a _ceiling_ and a _floor_ in a certain time window.


**Histogram/Timer**

A __histogram__ (as `prometheus` calls them) or __timer__ (as `statsd` calls them) is a metric
to track _sampled observations_. Unlike a __counter__ or a __gauge__, the value of a __histogram__ metric
doesn't necessarily show a pattern of going up or down. I know that doesn't make a lot of sense, 
especially how is it different from  __gauge__? The difference (it helps me think this way) is that
what you expect to do with histogram data is different from a gauge. The monitoring system thus needs
to know that a metric is of type __histogram__ type to be able to allow you to do these things.

![A histogram metric][histogram-graph.png]


## Demo 1

[Demo 1](https://github.com/amitsaha/python-monitoring-talk/tree/master/demo1) is
a basic web application written using the [Flask](http://flask.pocoo.org/) framework. It demonstrates how we can _calculate_ and _report_ metrics.

The `src` directory has the application in `app.py` with the `src/helpers/middleware.py` containing the following:

```

from flask import request
import csv
import time


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    # convert this into milliseconds for statsd
    resp_time = (time.time() - request.start_time)*1000
    with open('metrics.csv', 'a', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([str(int(time.time())), str(resp_time)])

    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(stop_timer)
```

When `setup_metrics()` is called from the application, it configures the
`start_timer()` function to be called before a request is processed and
the `stop_timer()` function to be called after a request is processed
but before the response has been sent. In the above function, we write
the `timestamp` and the time it took (in milliseconds) for the request
to be processed.

When we run `docker-compose up` in the `demo1` directory, it starts the web 
application and then starts a client container which makes a number of requests
to this web application. You will see a file `src/metrics.csv` that has been
created with two columns: `timestamp` and `request_latency`.

Looking at this file, we can infer two things:

- There is a lot of data that has been generated
- Each observation of the metric doesn't have any characteristic associated with it

Without characteristic associated with a metric observation, we cannot say which
HTTP endpoint this metric was associated with or which node of the application
this metric was generated from. Hence, we need to qualify each metric observation with the appropriate metadata.

## Overview of statistics

If we go back to high school mathematics, there were a few things that we probably all can recall
even if vaguely - __mean__, __median__, __percentile__ and __histograms__. Let's briefly recap what
these are without judging their usefulness, just like high school:

### Mean

The __mean__ or the average of a list of numbers is the sum of the numbers divided by the
cardinality of the list. The __mean__ of 3, 2, 10 is (3+2+10)/3 = 5.


### Median

The __median__ is another form of average, but is calculated differently. For our list above,
the median is 3. The calculation is not very straightforward - it depends on the number of items
in the list.


### Percentile

The __percentile__ is a measure which gives us a measure below which a certain, `k` percentage of the
numbers lie. In some sense, it gives us an _idea_ how this measure is doing relative to the `k` percentage
of our data. For example, the 95 percentile score of the above list is 9.29999. The percentile measure
varies between 0 to 100 (non-inclusive). The _zeroth_ percentile is the minimum score in a set of numbers.
Some of you may recall that the __median__ is the 50th percentile - which turns out to be 3.

Some monitoring systems refer to the percentile measure as `upper_X` where _X_ is the percentile.

### Quantile

The __q-Quantile__ is a measure which ranks q*N in a set of N numbers. The value of __q__ ranges between 0 and 1 
(both inclusive). When _q__ is 0.5, the value is the __median__. The relationship between the quantile and
percentile is that the measure at __q__ quantile is equivalent to the measure at __100*q__ percentile.

### Histogram

The metric of type __histogram__ which we learned about earlier is an _implementation detail_ of monitoring
systems. In statistics, a __histogram__ is a graph that groups data into _buckets_. Let's consider a different contrived example 
now - age of a group of people reading your blog. If you somehow managed to get a handful of this data 
and wanted a rough idea of the age group your readers belonged to, plotting a __histogram__ would show you
a graph like this:

![A histogram][histogram.png]


### Cumulative Histogram

A __cumulative histogram__ is a histogram with each bucket's count also including the count of the previous
bucket - hence the name, _cumulative_. A __cumulative histogram__ for the same data set above looks as follows:

![Cumulative histogram][cumulative-histogram.png]


### Why do we need statistics?

In `Demo 1` above, we observed that there is a lot of data that is generated
when we report metrics. We need statistics when working with metrics because there are just too many of them. We don't care about individual values, but in the overall behavior. We expect the behavior they exhibit is a proxy of the
behavior of the system under observation.

## Adding characteristics to metrics

Cosnsidering our `Demo 1` application above, when we calculate and report a request
latency, it refers to a specific request uniquely identified by few _characteristics_. Some of these are:

- The HTTP endpoint
- The HTTP Method
- The identifier of the host/node it is running on

If we attach these characteristics to a metric observation, we have more context
around each metric. Let's explore adding characteristics to our metrics in the next
demo, [Demo 2](https://github.com/amitsaha/python-monitoring-talk/tree/master/demo2).

THe `src/helpers/middleware.py` file now writes multiple columns to the CSV file
when writing metrics:

```
node_ids = ['10.0.1.1', '10.1.3.4']


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    # convert this into milliseconds for statsd
    resp_time = (time.time() - request.start_time)*1000
    node_id = node_ids[random.choice(range(len(node_ids)))]
    with open('metrics.csv', 'a', newline='') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([
            str(int(time.time())), 'webapp1', node_id,
            request.endpoint, request.method, str(response.status_code),
            str(resp_time)
        ])

    return response
```

As this is a demo, I have taken liberty of reporting one of two random IPs as
the node IDs when reporting the metric. When we run `docker-compse up` in the
`demo2` directory, it will result in a CSV file which will have multiple columns.

### Analaysing metrics with `pandas`

We are going to now analyse this CSV file with [pandas](https://pandas.pydata.org/).
When we run `docker-compose up`, we will see a URL printed which we will use
to open up a a [Jupyter]() session. Once we upload the `Analysis` notebook into
the session, we can read the CSV file into a pandas DataFrame:

```

```

Since each characteristic we added is a column in the DataFrame, we can perform
grouping and aggregation based on these columns:

## What should I monitor

A software system has a number of variables whose values change during its lifetime. We have the software
running in some sort of a operating system, so we have variables that change in the operating system as well.
Overall, in my opinion the more data you have, the better it is when something goes wrong.

Key operating system metrics that I consider should be monitored are:


- CPU usage
- System memory usage 
- File descriptor usage
- Disk usage

Then, depending on the software application, there will be a number of key metrics to monitor.

### Network applications 

If your software is a network application of some sort listening of client requests and serving
them, the key metrics to measure are:

- Number of requests coming in (__counter__)
- Unhandled errors (__counter__)
- Request latency (__histogram/timer__)
- Queued time - if there is a queue in your application (__histogram/timer__)
- Queue size - if there is a queue in your application (__gauge__)
- Worker processes/threads usage (__gauge__)

If your network application makes requests to other services in the context of fulfilling
a client request, it should have metrics to record the behavior of communication with these
services. Key metrics to monitor include number of requests, request latency and response status.


### HTTP web application backends

HTTP applications should monitor all of the above. In addition, it should keep granular data
about the count of non-200 HTTP statuses grouped by all the other HTTP status codes seen. If
your web application has a user signup and login functionality, it should have metrics for 
those as well.

### Long running processes

Long running processes such as a Rabbit MQ consumer or task queue workers, although not network
servers, they work on the model of picking up a task and processing it. Hence, we should monitor
the number of requests being processed and request latency for these kind of processes.

No matter the type of your application, each metric should have appropriate __metadata__ associated
with it.

## Integrating monitoring in your Python application

There are two components involved in integrating monitoring into your Python applications:

* Update your application to calculate and report metrics
* Setup a monitoring infrastructure to house your application's metrics and allow queries to be made against them

The basic idea of recording and reporting a metric is:

```python
def work():
    requests += 1
    # report counter
    start_time = time.time()
    
    # < do the work >

    # calculate and report latency
    work_latency = time.time() - start_time
    ...
```


Considering the above pattern, we will often find that we take advantage
of _decorators_, _context managers_ and _middleware_ (for network applications) to
calculate and report metrics. In Demo1 and Demo 2 above, we saw how we used
decorators in a Flask application.

### Pull and Push models for metric reporting

Essentially, there are two patterns for reporting metrics from a Python application:
![Pull and Push Models][pull_push_model.png]

An example of a monitoring system



### Integrating `statsd` into a Flask application




### Integrating prometheus into a Flask application


Given an `app` Flask application object, we can report calculate two example metrics as follows:


```python

REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)

def start_timer():
    request.start_time = time.time()

def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels('webapp', request.path).observe(resp_time)
    return response

# Register as middleware

app.before_request(start_timer)
app.after_request(record_request_data)
app.after_request(stop_timer)
```

# Uses of metrics

We briefly learned why we may want to setup monitoring in our applications. In this section,
we will look a bit deeper into two of these in this section.

### Using metrics for alerting

Once we have the metrics, one of the key things we want to do with them is to create __alerts__.
If the number of HTTP 500s over the past five minutes have been increasing, send an email or
a pager to the relevant person or team. What we use for setting up alerting depends on our monitoring
setup. For prometheus, we can use [alertmanager](https://github.com/prometheus/alertmanager) to create
alerts.

For statsd, we can setup alerts using [nagios](https://www.nagios.org/about/overview/).

### Using metrics for auto scaling

Not only can metrics allow us to understand if our current infrastructure is over provisioned
or under-provisioned, it also allows us to implement autoscaling policies in a cloud infrastructure
setup. For example, if our worker process usage in our servers have been routinely hitting 90%
for the past 5 minutes, may be we need to horizontally scale. How we would implement it depends
on the cloud infrastructure. AWS Auto Scaling groups by default allows scaling policies based on the system
CPU usage and network traffic among others. However, to use application metrics for scaling up
or down, we will need to publish [custom CloudWatch metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html).

## Application monitoring in a multi service architecture

When we go beyond a single application architecture such that a client request can trigger call to
multiple services before the response is sent back, we need more from our metrics. We want to have
a unified view of the latency metrics such that we can see how much time did each service take in
responding to the request. This is enabled by [distributed tracing](http://opentracing.io/documentation/). 

An example of getting started with distributed tracing in Python is shown in my 
[blog post](http://echorand.me/introducing-distributed-tracing-in-your-python-application-via-zipkin.html).


## Summary

I will end this article with the following points that we should keep in mind:

- Understand what a metric type means in your monitoring system
- Undersand what unit of measurement they want your data be sent in
- Monitor the most critical components of your application
- Monitor the behavior of your application in its most critical stages

The above is of course assuming that we don't have to manage our monitoring systems.
If that's part of our job, we have a lot more to think about!

## Resources

The following resources are some of the ones that I found very useful:

### General

- [Monitoring Distributed Systems](https://landing.google.com/sre/book/chapters/monitoring-distributed-systems.html)
- [Monitoring best practices](http://www.integralist.co.uk/posts/monitoring-best-practices/?imm_mid=0fbebf&cmp=em-webops-na-na-newsltr_20180309)
- [Who wants seconds?](https://www.robustperception.io/who-wants-seconds/)

### Statsd/Graphite

- [statsd metric types](https://github.com/etsy/statsd/blob/master/docs/metric_types.md)

### Prometheus

- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)
- [How does a prometheus gauge work?](https://www.robustperception.io/how-does-a-prometheus-gauge-work/)
- [Why are prometheus histograms cumulative?](https://www.robustperception.io/why-are-prometheus-histograms-cumulative/)
- [Monitoring batch jobs in Python](https://www.robustperception.io/monitoring-batch-jobs-in-python/)
- [Promtheus monitoring at soundcloud](https://developers.soundcloud.com/blog/prometheus-monitoring-at-soundcloud)
- [Why are Prometheus histograms cumulative?](https://www.robustperception.io/why-are-prometheus-histograms-cumulative/)

## Stage 3 Readings

As we learning the most important of basics of monitoring, we should also start looking at the mistakes
we don't want to make. Here are some insightful resources I have come across:

- [How not to measure latency](https://www.youtube.com/watch?v=lJ8ydIuPFeU&feature=youtu.be)
- [Histograms with Prometheus: A Tale of Woe](http://linuxczar.net/blog/2017/06/15/prometheus-histogram-2/)
- [Why Averages Suck and Percentiles are Great](https://www.dynatrace.com/news/blog/why-averages-suck-and-percentiles-are-great/)
- [Everything you know about latency is wrong](https://bravenewgeek.com/everything-you-know-about-latency-is-wrong/)
- [Who moved my 99th perecentile latency](https://engineering.linkedin.com/performance/who-moved-my-99th-percentile-latency)
- [Logs and metrics and graphs](https://grafana.com/blog/2016/01/05/logs-and-metrics-and-graphs-oh-my/)
- [HdrHistogram: A better latency capture method ](http://psy-lob-saw.blogspot.com.au/2015/02/hdrhistogram-better-latency-capture.html)
