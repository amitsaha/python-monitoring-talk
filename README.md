# Materials for my talks on Python monitoring

## Slides

- (Sydney Python Meetup)[]

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
