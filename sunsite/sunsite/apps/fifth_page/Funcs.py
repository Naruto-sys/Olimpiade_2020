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
    result = cur.execute(f"""SELECT area, indications FROM example_area WHERE city={city_num}""").fetchall()
    print(result)

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
    max2 = max(area1)
    max3 = max(area1)
    max4 = max(area1)

    x = np.arange(1, 5)
    y = np.array([max1, max2, max3, max4])

    fig, ax = plt.subplots()

    ax.bar(x, y, color='darkblue', width=0.2)

    plt.title(f'Максимальная температура, полученную в квартирах города {city_name}')

    plt.xlabel('Номер запроса (раз в полдня)')
    plt.ylabel('Температура, °C')

    fig.set_figwidth(20)
    fig.set_figheight(10)

    plt.savefig('plot.png', format='png')
