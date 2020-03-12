from django.shortcuts import render
from django.http import HttpResponse
from .models import Temperature, City
import requests
from .Funcs import check_response
import datetime
import time


def collection(request):
    HEADER = {'X-Auth-Token': 'qohuw6zrr4z74qn2'}
    LINK = 'https://dt.miet.ru/ppo_it/api/'
    link = 'https://dt.miet.ru/ppo_it/api/'
    response = requests.get(LINK, headers=HEADER)
    if not check_response(response):
        return HttpResponse("Error: " + str(response))

    first_time = datetime.datetime.now()
    while (datetime.datetime.now() - first_time).days < 1:
        time_iter = datetime.datetime.now()
        try:
            for city in response.json()['data']:
                city_id = city['city_id']
                city_name = city['city_name']
                link = LINK + str(city_id) + '/'
                response_city = requests.get(link, headers=HEADER)
                temperature = str(response_city.json()["data"]["temperature"])
                try:
                    obj = City.objects.get(city=city_id)
                    # '*' - разделение температур
                    data = obj.indications
                    obj.indications = data + '*' + temperature
                    obj.save()
                except Exception:
                    obj = City(city=city_id, indications=temperature)
                    obj.save()

                if not check_response(response_city):
                    continue

                for area in range(1, 5):
                    link = LINK + str(city_id) + '/' + str(area) + '/'
                    response_district = requests.get(link, headers=HEADER)

                    if not check_response(response_district):
                        continue

                    for home in range(1, 4):
                        house = response_district.json()['data'][home]
                        link1 = link + str(house["house_id"]) + '/'
                        response_house = requests.get(link1, headers=HEADER)

                        if not check_response(response_house):
                            continue

                        for flat in range(1, 4):
                            link2 = link1 + str(flat) + '/temperature/'
                            response_flat = requests.get(link2, headers=HEADER)

                            if not check_response(response_city):
                                continue

                            temperature = str(response_flat.json()['data'])

                            try:
                                obj = Temperature.objects.get(city=city_id, area=area, house=home, flat=flat)
                                # '*' - разделение температур
                                data = obj.indications
                                obj.indications = data + '*' + temperature
                                obj.save()
                            except Exception:
                                obj = Temperature(city=city_id, area=area, house=home, flat=flat, indications=temperature)
                                obj.save()
            if (datetime.datetime.now() - time_iter).seconds < 320:
                time.sleep(320 - (datetime.datetime.now() - time_iter).seconds)

        except Exception as e:
            continue
    return HttpResponse("Privet, Solnyshko! Vse Rabotaet!")


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
                city_number = str(town['city_id'])
                break

        final_link = LINK + city_number + '/' + area + '/' + house + '/' + flat + '/'
        final_response = requests.get(final_link, headers=HEADER)
        try:
            temperature = int(final_response.json()['data']['temperature'])
            temperature = str(final_response.json()['data']['temperature']) + '°'
        except Exception:
            temperature = 'Адрес введён некорректно!'

    context = {
        'temperature': temperature,
        'area': area,
        'house': house,
        'flat': flat,
        'city': city,
        'cities': cities,
        'submitbutton': submitbutton,
    }
    return render(request, 'first_page/first_page.html', context)
