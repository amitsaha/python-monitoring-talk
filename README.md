# Materials for my talks on Python monitoring

## Slides

- (Sydney Python Meetup)[./slides/sypy.pdf]

## Articles


## Playing with the demos

You will need `docker` and `docker-compse` installed. The following demos are available:

- [demo1](./demo1)
- [demo2](./demo2)
- [statsd](./statsd)
- [promtheus](./prometheus)
- [statsd_prometheus](./statsd_prometheus)

## Notes to self

### Docker tips

Rebuild an image:

```
$ docker-compose -f docker-compose.yml build
```

### ab tips

Make 100 requests with a concurrency of 3:

```
$ ab -n 100 -c 3 http://localhost:5000/test/

```

## Learn more

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

## Stage 3 Readings: Doing things right


- [How not to measure latency](https://www.youtube.com/watch?v=lJ8ydIuPFeU&feature=youtu.be)
- [Histograms with Prometheus: A Tale of Woe](http://linuxczar.net/blog/2017/06/15/prometheus-histogram-2/)
- [Why Averages Suck and Percentiles are Great](https://www.dynatrace.com/news/blog/why-averages-suck-and-percentiles-are-great/)
- [Everything you know about latency is wrong](https://bravenewgeek.com/everything-you-know-about-latency-is-wrong/)
- [Who moved my 99th perecentile latency](https://engineering.linkedin.com/performance/who-moved-my-99th-percentile-latency)
- [Logs and metrics and graphs](https://grafana.com/blog/2016/01/05/logs-and-metrics-and-graphs-oh-my/)
- [HdrHistogram: A better latency capture method ](http://psy-lob-saw.blogspot.com.au/2015/02/hdrhistogram-better-latency-capture.html)
