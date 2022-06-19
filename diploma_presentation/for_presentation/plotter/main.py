from NetStatsPlotter import NetStatsPlotter



if __name__ == '__main__':
    plotter = NetStatsPlotter("plots", "png")
    plotter.plot_net_stats("iperf.json")
    plotter.plot_queue_len("qlen.data")

