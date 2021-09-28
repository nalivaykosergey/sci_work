from mininet.topo import Topo
from mininet.link import TCLink

# Файл моделируемой топологии

class OwnTopology(Topo):

    def __init__(self, **opts):
        super(OwnTopology, self).__init__(**opts)
        
        #Создание узлов сети
        host1 = self.addHost('h%s' % 1)
        host2 = self.addHost('h%s' % 2)
        switch1 = self.addSwitch('s%s' % 1)
        # Соединение узлов с заданными характеристиками
        self.addLink(host1, switch1, cls=TCLink, bw=100, delay='25ms', loss=1, max_queue_size=50)
        self.addLink(host2, switch1, cls=TCLink, bw=100, delay='25ms', loss=1, max_queue_size=50)
        
