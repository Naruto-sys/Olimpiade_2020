import numpy as np
import matplotlib
import sqlite3
import shutil

matplotlib.use('Agg')

import matplotlib.pyplot as plt


def check_response(response):
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return False
    return True


def make_plot(city_num, city_name):
    con = sqlite3.connect(".\db.sqlite3")
    cur = con.cursor()
    result = cur.execute(f"""SELECT area, indications FROM first_page_temperature WHERE city={city_num}""").fetchall()

    area1 = []
    area2 = []
    area3 = []
    area4 = []

    for elem in result:
        if elem[0] == 1:
            area1.extend(int(_) for _ in elem[1].split('*'))
        if elem[0] == 2:
            area2.extend(int(_) for _ in elem[1].split('*'))
        if elem[0] == 3:
            area3.extend(int(_) for _ in elem[1].split('*'))
        if elem[0] == 4:
            area4.extend(int(_) for _ in elem[1].split('*'))

    max1 = max(area1)
    max2 = max(area2)
    max3 = max(area3)
    max4 = max(area4)

    x = np.arange(1, 5)
    y = np.array([max1, max2, max3, max4])

    fig, ax = plt.subplots()

    ax.bar(x, y, width=0.2)

    plt.title(f'Максимальная температура, полученная в квартирах города {city_name}')

    plt.xlabel('Номер запроса (раз в полдня)')
    plt.ylabel('Температура, °C')

    fig.set_figwidth(20)
    fig.set_figheight(6)

    plt.savefig('plot.png', format='png')
    shutil.move("plot.png", ".\static\imgs\plot.png")
    plt.close(fig)
