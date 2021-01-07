#!/bin/sh
ab -n 100 -c 4 http://service1:5000/
sleep 10
ab -n 1000 -c 4 http://service1-2:5000/
sleep 20
ab -n 100 -c 4 http://service1:5000/
