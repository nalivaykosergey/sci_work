from mininet.topo import Topo


class OwnTopology(Topo):

    def __init__(self, **opts):
        super(OwnTopology, self).__init__(**opts)
        host1 = self.addHost('h%s' % 1, cpu=.5 / 3, ip="10.0.0.1/8")
        host2 = self.addHost('h%s' % 2, cpu=.5 / 3, ip="10.0.0.2/8")
        host3 = self.addHost('h%s' % 3, cpu=.5 / 3, ip="10.0.0.3/8")
        switch1 = self.addSwitch('s%s' % 1)
        self.addLink(host1, switch1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
        self.addLink(host2, switch1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
        self.addLink(host3, switch1, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
