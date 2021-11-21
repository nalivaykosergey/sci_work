from time import sleep
from subprocess import *
import re
from threading import Thread
import os

default_dir = "monitoring"


def plot_data(iperf_data="iperf.json", qlen_data="qlen.dat"):
    if os.path.exists("{}/{}".format(default_dir, iperf_data)):
        cmd = "cd {} && plot_iperf.sh {}".format(default_dir, iperf_data)
        os.system(cmd)
    else:
        print("iperf file does not exists")
    if os.path.exists("{}/{}".format(default_dir, iperf_data)):
        cmd = "cd {} && gnuplot -c ../plot_qlen {} qlen.pdf".format(default_dir, qlen_data)
        os.system(cmd)
    else:
        print("qlen file does not exists")


class Monitor:

    def __init__(self, host, server, iface):

        if not os.path.exists(default_dir):
            os.makedirs(default_dir)
            os.system("chmod 777 {}".format(default_dir))
        self.host = host
        self.server = server
        self.iface = iface

    def qlen_monitoring(self, time=1, interval_sec_=0.1, fname="qlen.dat"):
        print("Начало мониторинга сети на интерфейсе {}. Продолжительность мониторинга: "
              "{} сек. с интервалом {}".format(self.iface, time, interval_sec_))
        current_time = 0
        # Регуляроное выражение для поиска данных с tc
        pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
        cmd = "tc -s qdisc show dev {}".format(self.iface)
        # Открытие файла мониторинга на запись
        file = open("{}/{}".format(default_dir, fname), 'w')
        # Цикл, в котором происходит мониторинг до прерывания
        while current_time < time:
            # Вызов команды в tc в терминале и поиск значения длины очереди, количества отброшенных пакетов
            p = Popen(cmd, shell=True, stdout=PIPE)
            output = p.stdout.read().decode('utf-8')
            matches_queue = pat_queued.findall(output)
            if matches_queue:
                t = "%f" % current_time
                current_time += interval_sec_
                file.write(t + ' ' + matches_queue[-1] + " " + '\n')
            sleep(interval_sec_)
            current_time += interval_sec_
        os.system("chmod 777 {}/{}".format(default_dir, fname))
        file.close()

    def iperf_monitoring(self, fname, params):
        print(
            "Начало работы iperf. Хост: {}, сервер: {}. Файл с данными: {}/{}".format(self.host.name, self.server.name,
                                                                                      default_dir, fname))
        self.server.cmd("iperf3 -s -D")
        self.host.cmd("iperf3 -c {} {} -J > {}/{}".format(self.server.IP(), params, default_dir, fname))
        os.system("chmod 777 {}/{}".format(default_dir, fname))

    def net_monitoring(self, iperf_file, iperf_commands, qlen_file, qlen_mon_time, qlen_mon_interval):
        th1 = Thread(target=self.iperf_monitoring, args=(iperf_file, iperf_commands,))
        th2 = Thread(target=self.qlen_monitoring, args=(qlen_mon_time, qlen_mon_interval, qlen_file))
        th1.start()
        th2.start()
        th1.join()
        th2.join()
        print("Мониторинг окончен")
