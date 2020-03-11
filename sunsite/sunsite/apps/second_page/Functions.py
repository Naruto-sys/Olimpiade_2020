import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from django.http import HttpResponse


def check_response(response):
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return False
    return True


def make_plot(city_num):
    con = sqlite3.connect(".\db.sqlite3")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM example_area""").fetchall()
    print(city_num)
    data = [int(_) for _ in result[city_num][-2].split('*')]

    x = np.arange(1, len(data) + 1)
    y = np.array(data)

    fig, ax = plt.subplots()

    ax.plot(x, y,
            linewidth=1,
            color='darkblue')

    plt.title('График температуры')

    plt.xlabel('Номер запроса')
    plt.ylabel('Температура')

    plt.grid()

    fig.set_figwidth(20)
    fig.set_figheight(6)

    plt.savefig('plot.png', format='png')
