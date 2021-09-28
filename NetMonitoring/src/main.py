from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from Model import OwnTopology


def simulation():
    topology = OwnTopology()
    net = Mininet(topo=topology, host=CPULimitedHost, link=TCLink)
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    simulation()
