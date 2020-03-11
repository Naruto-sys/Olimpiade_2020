from django.shortcuts import render
from django.http import HttpResponse
import requests
from .Funcs import make_plot


def main(request):
    LINK = 'https://dt.miet.ru/ppo_it/api/'
    HEADER = {'X-Auth-Token': 'qohuw6zrr4z74qn2'}
    response = requests.get(LINK, headers=HEADER)

    submitbutton = request.POST.get("submit")
    city = request.POST.get("city")
    area = request.POST.get("area")
    house = request.POST.get("house")
    flat = request.POST.get("flat")

    temperature = ''
    city_number = ''

    if area is None:
        area = ''
    if house is None:
        house = ''
    if flat is None:
        flat = ''

    cities = [_['city_name'] for _ in response.json()['data']]

    if city is not None:
        c = [cities[cities.index(city)]]
        [c.append(_) for _ in cities[:cities.index(city)]]
        [c.append(_) for _ in cities[cities.index(city) + 1:]]
        cities = c

    if submitbutton is not None:
        for town in response.json()['data']:
            if town['city_name'] == city:
                city_num = str(town['city_id'])
                break
        make_plot(city_num, city, area, house, flat)

    range1 = [str(_) for _ in range(1, 5)]
    range2 = [str(_) for _ in range(1, 4)]

    context = {
        'temperature': temperature,
        'area': area,
        'house': house,
        'flat': flat,
        'city': city,
        'cities': cities,
        'submitbutton': submitbutton,
        'range1': range1,
        'range2': range2
    }
    return render(request, 'fourth_page/fourth_page.html', context)

