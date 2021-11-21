from mininet.topo import Topo
import os


class OwnTopology(Topo):

    def __init__(self, config, **opts):
        super(OwnTopology, self).__init__(**opts)

        for i in config["devices"]:
            current = config["devices"][i]
            self.addHost(name=current["name"], ip=current["ip"])
        for i in config["switches"]:
            current = config["switches"][i]
            self.addSwitch(name=current["name"])

        for i in config["links"]["pairs"]:
            self.addLink(i[0], i[1])
