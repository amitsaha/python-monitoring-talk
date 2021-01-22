#!/bin/sh
sleep 20
ab -n 55 -c 1 http://service1:5000/
sleep 10
ab -n 20 -c 1 http://service1:5000/
sleep 10
ab -n 5 -c 1 http://service1-2:5000/
