# python-monitoring-talk

## Docker tips

Rebuild an image:

```
$ docker-compose -f docker-compose.yml build
```

## ab tips

Make 100 requests with a concurrency of 3:

```
$ ab -n 100 -c 3 http://localhost:5000/test/

```

