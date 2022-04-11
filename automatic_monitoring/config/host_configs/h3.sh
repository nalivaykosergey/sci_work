#!/bin/bash
sysctl -w net.ipv4.tcp_congestion_control=reno
sleep 10
iperf3 -c 10.0.0.4 -p 7779 -i 0.5 -t 10 -b 7mbit

