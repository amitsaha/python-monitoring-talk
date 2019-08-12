#!/bin/sh
ab -n 1000 -c 3 http://webapp:5000/test/
ab -n 1000 -c 3 http://webapp:5000/test1/
top
