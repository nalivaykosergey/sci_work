#!/bin/bash
sysctl -w net.ipv4.tcp_congestion_control=reno
sleep 5
iperf3 -c 10.0.0.4 -p 7778 -i 0.5 -t 10 -b 10mbit -J > out.json

