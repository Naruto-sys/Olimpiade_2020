from django.shortcuts import render
from django.http import HttpResponse
from .models import Area
import requests
from .Functions import check_response


def index(request):
    HEADER = {'X-Auth-Token': 'qohuw6zrr4z74qn2'}
    LINK = 'https://dt.miet.ru/ppo_it/api/'
    link = 'https://dt.miet.ru/ppo_it/api/'
    response = requests.get(LINK, headers=HEADER)
    if not check_response(response):
        return HttpResponse("Error: " + str(response))
    try:
        for city in response.json()['data']:
            city_id = city['city_id']
            city_name = city['city_name']
            link = LINK + str(city_id) + '/'
            response_city = requests.get(link, headers=HEADER)

            if not check_response(response_city):
                return HttpResponse("Error: " + str(response_city))

            for area in range(1, 5):
                link = LINK + str(city_id) + '/' + str(area) + '/'
                response_district = requests.get(link, headers=HEADER)

                if not check_response(response_district):
                    return HttpResponse("Error: " + str(response_district))

                for home in range(3):
                    house = response_district.json()['data'][home]
                    link1 = link + str(house["house_id"]) + '/'
                    response_house = requests.get(link1, headers=HEADER)

                    if not check_response(response_house):
                        return HttpResponse("Error: " + str(response_house))

                    for flat in range(1, 4):
                        link2 = link1 + str(flat) + '/temperature/'
                        response_flat = requests.get(link2, headers=HEADER)

                        if not check_response(response_city):
                            return HttpResponse("Error: " + str(response_city))

                        temperature = response_flat.json()['data']
                        # if Area.objects.get(city=city_id and area=area)


    except Exception as e:
        return HttpResponse("Error: " + e.__class__.__name__)

    return HttpResponse("Privet! Dasha! Rabotai!")

