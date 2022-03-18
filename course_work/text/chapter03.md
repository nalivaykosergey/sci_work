# Использование утилиты iproute2 для настройки интерфейсов сетевых элементов

## Общие сведения


$\quad$iproute2 --- это набор утилит для управления параметрами сетевых устройств в ядре Linux. Утилиты  разработаны в качестве унифицированного интерфейса к ядру Linux,  непосредственно управляющего  трафиком.

iproute2 заменил полный набор классических сетевых утилит UNIX, которые ранее использовались для настройки сетевых интерфейсов, таблиц маршрутизации и управления arp-таблицами: ifconfig, route, arp, netstat и др., предназначенных для создания IP-туннелей. iproute2 предлагает унифицированный синтаксис для управления  аспектами сетевых интерфейсов.

Набор утилит включает в себя три основные программы:

  - ip [@ip] --- утилита для просмотра параметров и конфигурирования сетевых интерфейсов, сетевых адресов, таблиц и правил маршрутизации, ARP-таблиц, IP-туннелей, адресов multicast рассылки, маршрутизации multicast-пакетов;
  - tc [@tc] --- утилита для просмотра и конфигурирования параметров управления трафиком,  позволяющая управлять классификацией трафика, дисциплинами управления очередями для различных классов трафика либо целиком для сетевого интерфейса, что, в свою очередь, позволяет реализовать QoS в нужном для системы объёме:
      - разделение разных типов трафика по классам;
      - назначение разных дисциплин обработки очередей трафика с разным приоритетом, механизмами прохождения очереди, ограничениями по скорости и т.п.;
  - ss [@ss] --- утилита для просмотра текущих соединений и открытых портов. <!--Аналог утилиты netstat.-->

## Утилита tc

$\quad$Утилита tc [@tc] наиболее полезна для исследования, так как она позволяет гибко настроить поведение контроля исходящего трафика. Система контроля трафика состоит из следующих компонентов.

  - Ограничения исходящего трафика (SHAPING). Когда трафик сформирован, его полоса пропускания начинает контролироваться. Ограничение может дать больше, чем уменьшение полосы пропускания - оно также используется для сглаживания пиков для более прогнозируемого поведения сети.
  - Планирования передачи пакетов (SCHEDULING). Это позволяет увеличить интерактивность исходящего трафика при гарантировании полосы пропускания для передачи данных большого объема. Такое упорядочение также называется приоритезацией и применяется для исходящего трафика.
  - Ограничения исходящего трафика (POLICING). Этот механизм позволяет ограничить количество пакетов или байт в потоке входящего трафика, соответствующих определенной классификации.
  - Отбрасывания (DROPPING). Трафик, превышающий установленную полосу пропускания, может быть отброшен как для входящего, так и исходящего трафика. Обработка трафика контролируется тремя типами объектов: очередями (qdiscs), классами и фильтрами.
Обработка трафика контролируется тремя типами объектов: очередями (qdiscs), классами и фильтрами.

Для информации о tc используется команда \mintinline{bash}{tc help}.

<!--
\begin{minted}[breaklines]{bash}
tc help
\end{minted}
-->

$\quad$Дисциплина очереди --- это алгоритм обработки очереди сетевых пакетов. Дисциплин на одном интерфейсе может быть задействовано несколько, а непосредственно к интерфейсу крепится корневая дисциплина (root qdisc). При этом каждый интерфейс имеет свою собственную корневую дисциплину. Каждой дисциплине и каждому классу назначается уникальный дескриптор (некоторый номер), который может использоваться последующими инструкциями для ссылки на эти дисциплины и классы. Помимо исходящей дисциплины, интерфейс так же может иметь и входящую дисциплину, которая производит управление входящим трафиком. Дисциплины на интерфейсе образуют иерархию, где в верху иерархии находится корневая дисциплина. Сам интерфейс ничего не знает о дисциплинах, находящихся под корневой, а поэтому работает только с ней.

Воспользуемся сетью Mininet из прошлой главы и с помощью tc выведем информацию о дисциплине очереди на сетевом устройстве s1-eth0 (интерфейс коммутатора, к которому подключен хост h1). Для этого воспользуемся командой

\begin{minted}[breaklines]{bash}
tc -s qdisc show dev s1-eth1
\end{minted}

На рис. [-@fig:0020] видно, что корневой дисциплиной очереди назначена дисциплина noqueue. Данная дисциплина означает «отправляй мгновенно, не ставь в очередь».

![Информация о дисциплине очереди на сетевом устройстве s1-eth0](iproute_tc_qdisc_show_s1-eth1.png){ #fig:0020 width=70% }

В выводе tc можно увидеть полезные для исследования данные:

- *Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0)* --- означает, что было отправлено 0 байт (0 пакетов), из которых 0 пакетов отброшено и 0 пакетов вышли за пределы лимита.
- *backlog 0b 0p requeues 0* --- размер очереди в байтах и пакетах.

Запомним параметр backlog: он будет полезен нам при сборе статистики.


## Виды дисциплин очередей

### Бесклассовые очереди

$\quad$Ниже перечислены виды бесклассовых очередей:

  - pfifo/bfifo --- простейшие очереди без обработки, лишь реализующие принцип «First In, First Out» (первый вошел -- первый вышел). Ограничены в пакетах или байтах.
  - pfifo_fast --- стандартная очередь ядра с ‘расширенным роутером’. Состоит из очереди с тремя потоками, учитывающей флаги типа услуги (Type of Service) и приоритет пакета.
  - RED --- Random Early Detection (случайное раннее обнаружение) симулирует физический затор, отбрасывая пакеты случайным образом при близком достижении заданной полосы пропускания. Хорошо подходит для приложений, требующих очень широкую полосу пропускания.
  - SFQ --- Stochastic Fairness Queueing (очередь равномерного случайного распределения пакетов) реорганизует трафик в очереди таким образом, что каждый ‘сеанс’ (‘session’, виртуальная подочередь) получает право отправить пакет, а маркер переходит на следующий сеанс.
  - TBF --- Token Bucket Filter (фильтр буфера токенов) удерживает скорость передачи пакетов на примерно постоянном уровне (меньшем, чем реальная скорость интерфейса). Хорошо масштабируется для широких каналов.

Подробнее о видах бесклассовых очередей можно прочесть в [@tc].

### Очереди с классами

$\quad$Ниже перечислены виды очередей с классами [@tc]:

  - CBQ --- очередь, базирующаяся на классах (Class Based Queueing), реализует мощную иерархию классов. Поддерживает ограничения и приоритеты. Разделение осуществляется по времени простоя канала, вычисляемого на основании среднего размера пакета и полосы пропускания.
  - HTB --- очередь (Hierarchy Token Bucket --- иерархический буфер токенов) реализует мощную иерархию классов с упором на согласование с существующей практикой. HTB обеспечивает гарантированную полосу пропускания для классов, также позволяет устанавливать верхние пределы межклассового разделения очереди. Содержит объекты ограничения, базирующиеся на TBF, и может устанавливать приоритеты для классов.
  - PRIO --- очередь может разделять трафик между тремя полосами, которые являются очередями любого типа. При извлечении пакета из очереди вначале исследуется подочередь с большим приоритетом, если в последней нет пакетов для обработки, то выбирается очередь с более низким приоритетом. Для установки приоритета используются биты типа услуги (Type of Service).

<!--Подробнее о видах очередей с классами можно прочесть в [@tc]. -->

## Пример построения иерархии дисциплин

$\quad$Построим простую топологию сети. Пусть, у нас имеется 2 хоста соединенные с сетью. Сеть состоит из двух коммутаторов с разными скоростями передачи данных. Назовем сетевые элементы как h1 (хост-передатчик), h2 (хост-приемник), s1 (коммутатор, соединенный с h1) и s2(коммутатор, соединенный с h2). Тогда сеть будет иметь следующие характеристики:

- скорость передачи данных от s1 к h1 равна 100 Мбит/c;
- скорость передачи данных от s1 к s2 равна 100 Мбит/c;
- скорость передачи данных от s2 к h2 равна 50 Мбит/c;
- задержка распространения между h1 и s1 равна 30 мс +- 7 мс;
- задержка распространения между s1 и s2 равна 30 мс +- 7 мс;
- процент потерь пакетов на каждом сетевом соединении равен 0.01%;
- дисциплиной очереди, которая установлена на интерфейсе s2-eth2, будет pfifo с максимальным количеством пакетов 30.

Скорость передачи на интерфейсе можно ограничить с помощью дисциплины tbf, а эмулировать задержки распространения и потери мы будем с помощью дисциплины NetEm. NetEm обеспечивает функциональность сетевой эмуляции для тестирования протоколов, имитируя свойства глобальных сетей.

1. Откроем MiniEdit и создадим простую топологию сети (рис. [-@fig:0030]).

![Топология сети](iproute_net_topo.png){ #fig:0030 width=70% }

2. Запустим сеть.
3. Введем следующие команды tc:


  \begin{minted}[breaklines,linenos]{bash}
  sudo tc qdisc replace dev s1-eth2 root handle 10: tbf rate 100mbit burst 50000 limit 150000
  sudo tc qdisc add dev s1-eth2 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal
  sudo tc qdisc replace dev s1-eth1 root handle 10: tbf rate 100mbit burst 50000 limit 150000
  sudo tc qdisc add dev s1-eth1 parent 10: handle 20: netem loss 0.01% delay 30ms 7ms distribution normal
  sudo tc qdisc replace dev s2-eth2 root handle 10: tbf rate 50mbit burst 25000 limit 75000
  sudo tc qdisc add dev s2-eth2 parent 10: handle 15: pfifo limit 30
  sudo tc qdisc replace dev s2-eth1 root handle 10: tbf rate 50mbit burst 25000 limit 75000
  \end{minted}

  Любая команда добавления дисциплины на интерфейс, работающая с бесклассовыми дисциплинами, имеет вид:

  \begin{minted}[breaklines]{bash}
  tc qdisc [add/replace] dev [interface] [root/parent num] handle [number]: [Queue Discipline] [discipline parameters]
  \end{minted}

  Параметры команды:

  - [add/replace] --- выбирается в зависимости от иерархии дисциплин. Если дисциплина еще не назначена --- ставим add, если требуется заменить существующую дисциплину --- ставим replace;
  - [interface] --- фактический сетевой интерфейс устройства;
  - [root/parent num] --- выбирается в зависимости от иерархии дисциплин. Если дисциплина должна быть назначена как корневая --- ставим root, если дисциплина должна прикрепиться к родителю --- ставим parent с дескриптором родителя;
  - [number] --- дескриптор, который мы назначаем на дисциплину;
  - [Queue Discipline] --- название дисциплины;
  - [discipline parameters] --- параметры дисциплины.

  TBF --- дисциплина, построенная на понятии токена и заполненности некоторого буфера, называемого ведром». Данные поступают на вход алгоритма, токены генерируются и поступают в «ведро». Если токен имеется в «ведре», то данные проходя на интерфейс и отправляются в сеть. Если «ведро» пусто, то пакеты ставятся в очередь. По достижению некоторого лимита очереди пакеты отбрасываются.

  Параметры tbf: 

  - rate --- фактическая скорость, с которой генерируются токены;
  - burst --- количество байтов, которое может поместиться в ведре;
  - limit --- размер очереди.

  Параметры netem:

  - loss --- процент потерь на соединении;
  - delay --- задержка распространения. В нашем примере запись *delay 30ms 7ms distribution normal* означает, что задержка равна 30 мс, при этом это значение варьируется от 23 до 37 мс с вероятностью, заданной нормальным распределением.


4. Запустим iPerf-клиет и iPerf-сервер (рис. [-@fig:0031]). Запишем данные в файл json и построим графики сетевых характеристик.

![Мониторинг сети](iproute_monitor.png){ #fig:0031 width=80% }

5. Рассмотрим, как изменилось поведение нашей сети в сравнении с из
   прошлым разделом, где рассматривалась идеальная сеть без заданных
   сетевых параметров (потерь, задержек, максимальной скорости
   передачи). <!--Здесь нас интересуют следующие графики:-->

  Окно перегрузки  (рис. [-@fig:0032]) достаточно долго не может найти оптимальное значение, так как происходят частые потери из-за увеличения размера очереди на коммутаторе. Так как по умолчанию на рабочей машине стоит алгоритм для работы с перегрузками TCP Reno, то видно что график принимает пилообразные очертания.

  ![График изменения значения окна перегрузки TCP Reno](iproute_cwnd.png){ #fig:0032 width=70% }

На рис. [-@fig:0033] приведен график изменения значения количества
повторно переданных данных с течением времени --- появились потери
пакетов на соединении, причем, достаточно частые.

  ![График изменения  количества повторно переданных данных](iproute_retransmits.png){ #fig:0033 width=70% }

Среднее значение RTT (рис. [-@fig:0034]) сильно увеличилось (0.04 мс против 60 мc), что  связано с мгновенной отправкой данных без задержки в очереди.

  ![График изменения значения RTT с течением времени](iproute_rtt.png){ #fig:0034 width=68% }

 Пропускная способность (рис. [-@fig:0035]) колеблется от 0 Мбит/с до
 70 мбит/c из-за  искусственного ограничения скорости
 передачи,  потерь в сети и задержек распространения.

  ![График изменения значения пропускной способности](iproute_throughput.png){ #fig:0035 width=70% }

## Измерение размера очереди на дисциплине

$\quad$Некоторые сетевые характеристики мы уже успели рассмотреть в прошлой главе. Однако, иногда для анализа работы сети оказывается полезной еще одна характеристика, которую мы не можем измерить с помощью iPerf, так как данных по ней попросту нет ни на хосте, ни на сервере. Речь идет о длине очереди на сетевом устройстве.

Задача разработчиков сети --- достигнуть оптимальной скорости передачи данных с минимально возможной задержкой. Одним из факторов, который сказывается на это, является очередь на коммутаторах/маршрутизаторах. Буфер в коммутаторе (место, куда поступают пакеты и становятся в очередь на обслуживание) помогает не потерять пакеты, если имеет место высокая интенсивность поступления трафика. Если сеть работает на пределе, очередь коммутатора/маршрутизатора будет заполнена и пакеты начнут теряться. Чем длиннее очередь, тем больше задержка, что в свою очередь сильно сказывается на общей пропускной способности сети.

Реакцию очереди на изменение конфигураций передачи данных можно измерить и в зависимости от результатов подстроить другие параметры для достижения лучшей работы сети в целом. Например, изменив алгоритм работы с перегрузками на хостах, или дисциплину очереди, можно достичь лучшей производительности сети.

Для измерения длины очереди полезным окажется вывод статистики tc. Запись backlog указывает на размер очереди дисциплины в байтах и пакетах. Это статистику можно снять и измерять каждый промежуток времени с помощью функции на любом языке программирования. Функция записывает время и размер очереди в файл, с помощью которого легко построить график, например, в gnuplot.

Напишем функцию, которая замеряет размер очереди с заданным интервалом времени. Диграмма активностостей для такой функции приведена на рис. [-@fig:0036]. С помощью скрипта на языке программирования python ([см. приложение В](#appendix2)) построим график изменения длины очереди на интерфейсе [-@fig:0037].

Настройки сети аналогичны сети из прошлой главы (включая настройки qdisc).

![Диаграмма активностей для функции замеров длины очереди](iproute_act_dia.png){ #fig:0036 width=90% }

![График изменения длины очереди на интерфейсе s2-eth2](iproute_queue_len.png){ #fig:0037 width=70% }

На графике видно, что в определенные моменты времени длина очереди или возрастает, или убывает. Связано это с алгоритмом TCP Reno. При высокой загруженности канала связи увеличивается длина очереди и, как следствие, RTT. В момент, когда RTT переходит за допустимую норму, источник уменьшает окно перегрузки, что влечет за собой уменьшение битрейта и длины очереди.