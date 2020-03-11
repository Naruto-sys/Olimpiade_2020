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
    result = cur.execute(f"""SELECT indications FROM example_area WHERE city={city_num}""").fetchall()

    data = []
    for elem in result:
        string = elem[0]
        data.append([int(_) for _ in string.split("*")])

    new_data = []
    for i in range(len(max(data))):
        count = 0
        summ = 0
        for j in range(36):
            try:
                a = data[j][i]
            except IndexError:
                break
            summ += data[j][i]
            count += 1
        if count != 0:
            new_data.append(summ // count)

    data = new_data
    x = np.arange(1, len(data) + 1)
    y = np.array(data)

    fig, ax = plt.subplots()

    ax.plot(x, y, linewidth=1)

    plt.title(f'График средней температуры в квартирах в городе {city_name}')

    plt.xlabel('Номер запроса (раз в полдня)')
    plt.ylabel('Температура, °C')

    plt.grid()

    fig.set_figwidth(20)
    fig.set_figheight(6)

    plt.savefig('plot.png', format='png')
    shutil.move("plot.png", ".\static\imgs\plot.png")
    plt.close(fig)
