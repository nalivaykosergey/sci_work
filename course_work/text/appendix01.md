# Построение графиков сетевых характеристик из полученных данных iPerf3{#appendix1}

$\quad$Имея данные в формате json их обработка на языке программирования python сводится к тривиальной. Первым делом мы подключаем модуль json к программе, с помощью метода load загружаем данные переменную. На выходе у нас имеется готовый список данных, обработка которых представляет собой выбор по ключевому полю данных и их запись в нужную переменную. Код для функции обработки данных представлен ниже. 

\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
'''
    Функция обработки данных iPerf.
    Данные обрабатываются из предположения, что нас
    интересуют только данные, перечисленные в 
    словаре y. Функция возвращает словарь [x,y].
'''
def parse_netstat_file(net_data_file):
    raw_data = json.load(net_data_file)
    x = []
    y = {
        "bytes": [[], 
        {"title": "Количество переданных байт", "x": "Время (с)", "y": "MB"}],
        "cwnd": [[], 
        {"title": "Окно перегрузки", "x": "Время (с)", "y": "cwnd"}],
        "MTU": [[], 
        {"title": "Максимальный размер пакета", "x": "Время (с)", "y": "B"}],
        "retransmits": [[], 
        {"title": "Повторно переданные пакеты", "x": "Время (с)", "y": "Количество пакетов"}],
        "rtt": [[], 
        {"title": "Круговая задержка", "x": "Время (с)", "y": "ms"}],
        "rttvar": [[], 
        {"title": "Отклонение круговой задержки", "x": "Время (с)", "y": "ms"}],
        "throughput": [[], 
        {"title": "Пропускная способность", "x": "Время (с)", "y": "MBits"}]
    }
    '''
        Цикл считывания данных из json-файла.
        В список x сохраняются временные данные, а 
        в словарь y - все остальные. Характеристи для y
        нормируются в зависимости от требуемой 
        шкалы измерения данных.
    '''
    for i in raw_data["intervals"]:
        tmp_data = i["streams"][0]
        x.append(tmp_data["start"])
        y["bytes"][0].append(tmp_data["bytes"] / 1024 / 1024)
        y["cwnd"][0].append(tmp_data["snd_cwnd"] / 1024)
        y["MTU"][0].append(tmp_data["pmtu"])
        y["retransmits"][0].append(tmp_data["retransmits"])
        y["rtt"][0].append(tmp_data["rtt"] / 1000)
        y["rttvar"][0].append(tmp_data["rttvar"] / 1000)
        y["throughput"][0].append(tmp_data["bits_per_second"] / 1000000)
    return [x, y]
\end{minted}

Получив обработанные данные, мы можем построить графики. Код для функции построения графиков представлен ниже.

\begin{minted}
[
frame=lines,
framesep=2mm,
baselinestretch=1.2,
fontsize=\footnotesize,
linenos
]
{python}
'''
    Функция построения графиков сетевых характеристик.
    На вход поступает список значений, где первый элемент -
    время, а второй элемент - список значений сетевых 
    характеристик.
    Графики сохраняются в заданном формате 
    (параметр plot_format) и в заданную 
    директорию (параметр folder)
'''
def plot_net_stats(stats, plot_format, folder):
    x_stats, y_stats = stats
    for i in y_stats:
        plt.plot(x_stats, y_stats[i][0], 'k', linewidth=1)
        plt.grid()
        plt.xlim(xmin=0, xmax=x_stats[-1])
        plt.xlabel(y_stats[i][1]["x"])
        plt.ylabel(y_stats[i][1]["y"])
        plt.title(y_stats[i][1]["title"])
        plt.savefig("{}{}.{}".format(folder, i, plot_format))
        plt.clf()
\end{minted}

Теперь мы можем соединить эти функци воедино в скриптовом файле, выбрать целевой файл, передать параметры для функций и построить графики сетевых характеристик. 