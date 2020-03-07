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

            for i in range(1, 5):
                link = LINK + str(city_id) + '/' + str(i) + '/'
                response_district = requests.get(link, headers=HEADER)

                if not check_response(response_district):
                    return HttpResponse("Error: " + str(response_district))

                for j in range(3):
                    house = response_district.json()['data'][j]
                    link1 = link + str(house["house_id"]) + '/'
                    response_house = requests.get(link1, headers=HEADER)

                    if not check_response(response_house):
                        return HttpResponse("Error: " + str(response_house))

                    for k in range(1, 4):
                        link2 = link1 + str(k) + '/temperature/'
                        response_flat = requests.get(link2, headers=HEADER)

                        if not check_response(response_city):
                            return HttpResponse("Error: " + str(response_city))

                        temperature = response_flat.json()['data']

    except Exception as e:
        return HttpResponse("Error: " + e.__class__.__name__)

    return HttpResponse("Privet! Dasha! Rabotai!")

