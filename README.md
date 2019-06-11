# Materials for my talks/articles on Python monitoring

## Videos

- [PyCOn 2018](https://www.youtube.com/watch?reload=9&v=R4kMwckrUlg)

## Slides

- [PyCon 2018](./slides/pycon-2018.pdf)
- [Sydney Python Meetup - March, 2018](./slides/sypy.pdf)

## Articles

- [Understanding metrics and monitoring with Python](https://opensource.com/article/18/4/metrics-monitoring-and-python)
- [Exploring Security, Metrics, and Error-handling with gRPC in Python](https://blog.codeship.com/exploring-security-metrics-and-error-handling-with-grpc-in-python/)
- [Your options for monitoring multi-process Python applications with Prometheus](http://echorand.me/your-options-for-monitoring-multi-process-python-applications-with-prometheus.html)
- [Monitoring Your Synchronous Python Web Applications Using Prometheus](https://blog.codeship.com/monitoring-your-synchronous-python-web-applications-using-prometheus/)
- [Monitoring Your Asynchronous Python Web Applications Using Prometheus](https://blog.codeship.com/monitoring-your-asynchronous-python-web-applications-using-prometheus/)

## Playing with the demos

I recommend using a VM to play with the demos. This repo ships with a [Vagrantfile](./Vagrantfile)
for installing Ubuntu 16.04. Please install [Vagrant](https://vagrantup.com) for your operating system and then:

### VM Setup on Windows 10 with Hyper-V

You will need to open a powershell session as Adminstrator and do the following from a clone of 
the git repository:

```
C:\> ~\work\github.com\amitsaha\python-monitoring-talk [master ≡]> vagrant up --provider=hyperv
Bringing machine 'default' up with 'hyperv' provider...
==> default: Verifying Hyper-V is enabled...
==> default: Importing a Hyper-V instance
    default: Please choose a switch to attach to your Hyper-V instance.
    default: If none of these are appropriate, please open the Hyper-V manager
    default: to create a new virtual switch.
    default:
    default: 1) Default Switch
    default: 2) nat
    default: 3) minikube-virtualswitch
    default:
    default: What switch would you like to use? 1
    default: Cloning virtual hard drive...
    default: Creating and registering the VM...
    default: Setting VM Integration Services
    default: Successfully imported a VM with name: ubuntu-18.04-amd64_1
==> default: Starting the machine...
==> default: Waiting for the machine to report its IP address...
    default: Timeout: 120 seconds
```

Then, we will `ssh` into the VM using:

```
C:\> ~\work\github.com\amitsaha\python-monitoring-talk [master ≡]> vagrant ssh
```
    
### VM Setup on Windows/Linux/OS X - VirtualBox

```
$ vagrant up
...
$ vagrant ssh
```


Now, that we are in the VM, the `/vagrant` directory has a copy of the entire repository from where you
can play with the demos:

```
$ cd /vagrant
$ ls
demo1  LICENSE                 prometheus  scripts  statsd             Vagrantfile
demo2  opensource-com-article  README.md   slides   statsd_prometheus
```

Demos:

- [demo1](./demo1)
- [demo2](./demo2)
- [statsd](./statsd)
- [promtheus](./prometheus)
- [statsd_prometheus](./statsd_prometheus)

Each demo directory above has a README explaining the instructions of playing with the demo. In general,
to access a network port running in the virtual machine, use the following address in your browser:

```
$ 127.0.0.1:port
```

If it doesn't work, please file an issue with OS + VM details.

## Miscellaneous notes



### Docker tips

Rebuild an image:

```
$ sudo docker-compose -f docker-compose.yml build
```

If you see errors such as:

```ERROR: for webapp  Cannot create container for service webapp: Conflict. The container name "/webapp" is already in use by container "2e452aa1622b053fe33c6fe508ddce3f207e8a8c7446564f86e6f31c2d81466c". You have to remove (or rename) that container to be able to reuse that name.```

You can do:

```
$ sudo docker rm webapp
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
