#!/bin/sh
ab -n 100 -c 2 http://service1:5000/
sleep 10
ab -n 100 -c 2 http://service1:5000/
sleep 20
ab -n 100 -c 2 http://service1:5000/