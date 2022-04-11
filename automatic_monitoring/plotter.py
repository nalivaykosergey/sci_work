import monitoring.NetDataParser
import monitoring.NetDataPlotting
from sys import argv


if __name__ == "__main__":
    filename = argv[1]
    data = monitoring.NetDataParser.parse_netstat_file(filename)
    monitoring.NetDataPlotting.plot_net_stats(data, "pdf", "some_dir")