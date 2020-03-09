from django.shortcuts import render
from django.http import HttpResponse
from .models import Area, City
import requests
from .Functions import check_response
import datetime
import time
from .forms import UserForm


def index(request):
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
                                obj = Area.objects.get(city=city_id, area=area, house=home, flat=flat)
                                # '*' - разделение температур
                                data = obj.indications
                                obj.indications = data + '*' + temperature
                                obj.save()
                            except Exception:
                                obj = Area(city=city_id, area=area, house=home, flat=flat, indications=temperature)
                                obj.save()
            if (datetime.datetime.now() - time_iter).seconds < 320:
                time.sleep(320 - (datetime.datetime.now() - time_iter).seconds)

        except Exception as e:
            continue
    return HttpResponse("Privet! Solnishko! Rabotai!")


def main(request):
    submitbutton = request.POST.get("submit")

    firstname = ''
    lastname = ''
    emailvalue = ''

    form = UserForm(request.POST or None)
    if form.is_valid():
        firstname = form.cleaned_data.get("first_name")
        lastname = form.cleaned_data.get("last_name")
        emailvalue = form.cleaned_data.get("email")

    context = {'form': form, 'firstname': firstname,
               'lastname': lastname, 'submitbutton': submitbutton,
               'emailvalue': emailvalue}

    return render(request, 'example/page.html', context)