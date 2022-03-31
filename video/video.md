# Пример 1. NETEM + TBF (Технические моменты)

h1-s1-h2

sudo tc qdisc replace dev s1-eth2 root handle 10: tbf rate 100mbit burst 50000 limit 150000
sudo tc qdisc add dev s1-eth2 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal

sudo tc qdisc replace dev s1-eth1 root handle 10: tbf rate 100mbit burst 50000 limit 150000
sudo tc qdisc add dev s1-eth1 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal


# pfifo

sudo tc qdisc replace dev s1-eth2 root handle 10: tbf rate 100mbit burst 50000 limit 150000
sudo tc qdisc add dev s1-eth2 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal
sudo tc qdisc replace dev s1-eth1 root handle 10: tbf rate 100mbit burst 50000 limit 150000
sudo tc qdisc add dev s1-eth1 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal

sudo tc qdisc replace dev s2-eth2 root handle 10: tbf rate 50mbit burst 25000 limit 75000
sudo tc qdisc add dev s2-eth2 parent 10: handle 15: pfifo limit 30

sudo tc qdisc replace dev s2-eth1 root handle 10: tbf rate 50mbit burst 25000 limit 75000

### RED

sudo tc qdisc replace dev s1-eth2 root handle 10: tbf rate 100mbit burst 50000 limit 150000
sudo tc qdisc add dev s1-eth2 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal
sudo tc qdisc replace dev s1-eth1 root handle 10: tbf rate 100mbit burst 50000 limit 150000
sudo tc qdisc add dev s1-eth1 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal

sudo tc qdisc replace dev s2-eth2 root handle 10: tbf rate 50mbit burst 25000 limit 75000
sudo tc qdisc add dev s2-eth2 parent 10: handle 15: red limit 60Mbit avpkt 1000 probability 0.1 bandwidth 100Mbit

sudo tc qdisc replace dev s2-eth1 root handle 10: tbf rate 50mbit burst 25000 limit 75000

# usage:

./qlen_monitor s1-eth1 0.1 qlen1.txt
gnuplot -c plot_qlen qlen1.txt qlen1.pdf
