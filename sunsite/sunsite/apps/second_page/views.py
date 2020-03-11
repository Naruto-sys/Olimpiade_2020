from django.shortcuts import render
import requests
from .Functions import make_plot


def main(request):
    LINK = 'https://dt.miet.ru/ppo_it/api/'
    HEADER = {'X-Auth-Token': 'qohuw6zrr4z74qn2'}
    response = requests.get(LINK, headers=HEADER)

    submitbutton = request.POST.get("submit")
    city = request.POST.get("city")

    city_number = ''

    cities = [_['city_name'] for _ in response.json()['data']]

    if city is not None:
        c = [cities[cities.index(city)]]
        [c.append(_) for _ in cities[:cities.index(city)]]
        [c.append(_) for _ in cities[cities.index(city) + 1:]]
        cities = c

    if submitbutton is not None:
        for town in response.json()['data']:
            if town['city_name'] == city:
                city_number = str(town['city_id'])
                break
        make_plot(int(city_number), city)

    context = {
        'city': city,
        'cities': cities,
        'submitbutton': submitbutton,
    }
    return render(request, 'second_page/second_page.html', context)
