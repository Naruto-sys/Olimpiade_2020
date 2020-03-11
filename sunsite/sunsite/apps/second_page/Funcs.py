import numpy as np
import matplotlib.pyplot as plt
import sqlite3


def check_response(response):
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return False
    return True


def make_plot(city_num, city_name):
    con = sqlite3.connect(".\db.sqlite3")
    cur = con.cursor()
    result = cur.execute(f"""SELECT indications FROM example_city WHERE city={city_num}""").fetchall()
    data = [int(_) for _ in result[0][0].split('*')]

    x = np.arange(1, len(data) + 1)
    y = np.array(data)

    fig, ax = plt.subplots()

    ax.plot(x, y, linewidth=1, color='darkblue')

    plt.title(f'График температуры в городе {city_name}')

    plt.xlabel('Номер запроса (раз в полдня)')
    plt.ylabel('Температура, °C')

    plt.grid()

    fig.set_figwidth(20)
    fig.set_figheight(6)

    plt.savefig('plot.png', format='png')
