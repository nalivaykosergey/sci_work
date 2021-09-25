from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from Model import OwnTopology
from Monitor import Monitor



def simulation():
    topology = OwnTopology()
    net = Mininet(topo=topology, host=CPULimitedHost, link=TCLink)
    monitor = Monitor()

    net.start()
    monitor.monitoring_qlen(interval_sec=0.1)

    h1, h2 = net.get('h1', 'h2')
    monitor.iperf_output(h1, h2,  "-t 20")

    monitor.stop_monitoring()
    net.stop()



if __name__ == '__main__':
    simulation()
