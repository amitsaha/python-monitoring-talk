 Demo 2

This demo builds upon [Demo 1](../demo1). It demonstrates:

- Adding *characteristics* to metrics
- Analyzing the metrics using [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)

## Adding characteristics to metrics

We update the [middlware.py](./src/helpers/middleware.py) to add characteristics to our data as follows:


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
...
```


## Run demo

- `$ sudo docker-compose up`

## Play with the data

`docker-compose` run will print a URL which you can copy-paste into the browser on
our host.

Then, open the `Analysis` Jupyter Notebook by navigating to the `demo2` directory.
