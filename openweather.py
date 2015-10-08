#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import time


convert_day = {
    'Sun': 'Воскресенье',
    'Mon': 'Понедельник',
    'Tue': "Вторник",
    'Wed': 'Среда',
    'Thu': 'Четверг',
    'Fri': 'Пятница',
    'Sat': 'Суббота'
}


convert_month = {
    'Jan': 'Января',
    'Feb': 'Февраля',
    'Mar': 'Марта',
    'Apr': 'Апреля',
    'May': 'Мая',
    'Jun': 'Июня',
    'Jul': 'Июля',
    'Aug': 'Августа',
    'Sep': 'Сентября',
    'Oct': 'Октября',
    'Nov': 'Ноября',
    'Dec': 'Декабря'
}


def get_html():
    """Загружаем страницу с погодой"""
    req = Request('http://api.openweathermap.org/data/2.5/forecast/daily?q=Yekaterinburg&mode=json&units=metric&cnt=6')

    try:
        response = urlopen(req)

    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        exit(0)

    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        exit(0)

    global result, len_list
    result = json.loads(response.read().decode('utf8'))
    len_list = len(result['list'])


def sep(n):
    """Сепаратор"""
    print ('-' * n)


def header():
    """Вывод заголовка таблицы"""
    sep(90)
    print('Дата'.ljust(30) + 'Днем'.ljust(10) + 'Ночью'.ljust(10) + 'Ветер'.ljust(10) + 'Погодные условия')
    sep(90)


def footer():
    """Вывод футера таблицы"""
    sep(90)
    print ('Погода загружена с openweathermap.org ')
    sep(90)


def out_weather():
    """Значения температур и скорости ветра округлены"""
    day = str(time.strftime('%d', time.localtime(result['list'][i]['dt']))) # Дата
    weekday = convert_day[time.strftime('%a', time.localtime(result['list'][i]['dt']))]  # День недели
    month = convert_month[time.strftime('%b', time.localtime(result['list'][i]['dt']))]  # Месяц

    day = str(weekday) + ', ' + str(day) + ' ' + str(month)
    temp_day = (str(round(result['list'][i]['temp']['day']))) + ' C'  # Дневная температура
    temp_night = (str(round(result['list'][i]['temp']['night']))) + ' C'  # Ночная температура
    wind_speed = (str(round(result['list'][i]['speed']))) + ' м/с'  # Скорость ветра
    weather_parameters = (result['list'][i]['weather'][0]['main'])  # Облачно, солнечно и т.д.
    weather_parameters_description = (result['list'][i]['weather'][0]['description'])  # Более подробно

    return\
        day.ljust(30) + \
        temp_day.ljust(10) + \
        temp_night.ljust(10) + \
        wind_speed.ljust(10) + \
        weather_parameters + \
        '(' + weather_parameters_description + ')'


if __name__ == "__main__":

    get_html()
    header()

    for i in range(len_list):
        print (out_weather())

footer()

