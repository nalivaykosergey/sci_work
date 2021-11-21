from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from Model import OwnTopology
from Monitor import Monitor, plot_data
import sys
import toml
import os


def configure_links(config):
    for i in config["root"]["cmd"]:
        os.system(i)


def configure_device(config, device):
    for i in config["devices"][device.name]["cmd"]:
        device.cmd(i)


def simulation(config):
    topology = OwnTopology(config)
    net = Mininet(topo=topology, host=CPULimitedHost, link=TCLink)
    net.start()
    configure_links(config)

    h1, h2 = net.get('h1', 'h2')
    configure_device(config, h1)
    configure_device(config, h2)
    monitor = Monitor(h1, h2, "s2-eth2")

    iperf_file = "iperf.json"
    iperf_commands = "-t 10"
    qlen_file = "qlen.data"
    qlen_mon_time = 10
    qlen_mon_interval = 0.01
    monitor.net_monitoring(iperf_file, iperf_commands, qlen_file, qlen_mon_time, qlen_mon_interval)

    plot_data(iperf_file, qlen_file)

    net.stop()


if __name__ == '__main__':
    if os.path.exists(sys.argv[1]):
        config_file = toml.load(sys.argv[1])
        simulation(config_file)
    else:
        print("Конфигурационный файл не найден!")
