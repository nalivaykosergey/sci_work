from time import sleep, time
from subprocess import *
import re
from threading import Thread



default_dir = '.'
class Monitor:

    def __init__(self):
        self.processes = []
        self.flag = True
    def monitoring_qlen(self, iface='s1-eth1', interval_sec=0.01, filename='%s/qlen.txt' % default_dir):
        def func(iface_, interval_sec_, fname_):
            current_time = 0
            pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
            cmd = "tc -s qdisc show dev %s" % iface_
            ret = []
            open(fname_, 'w').write('')
            while self.flag:
                try:
                    p = Popen(cmd, shell=True, stdout=PIPE)
                    output = p.stdout.read().decode('utf-8')
                    matches = pat_queued.findall(output)
                    if matches and len(matches) > 1:
                        ret.append(matches[1])
                        t = "%f" % current_time
                        current_time += interval_sec_
                        open(filename, 'a').write(t + ' ' + matches[1] + '\n')
                    sleep(interval_sec_)
                except KeyboardInterrupt:
                    break
        prc = Thread(target=func, args=(iface, interval_sec, filename, ))
        self.processes.append(prc)
        prc.start()

    def iperf_output(self, client, server, params="",  filename="%s/file.json" % default_dir):
        server.cmd("iperf3 -s -D")
        client.cmd("iperf3 -c {} {} -J > {}".format(server.IP(), params, filename))

    def stop_monitoring(self):
        self.flag = False
        for i in self.processes:
            i.join()
