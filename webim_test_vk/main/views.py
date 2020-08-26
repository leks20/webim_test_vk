import os
from json import JSONDecodeError

import requests
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from requests import exceptions

load_dotenv()
VK_TOKEN = os.getenv('VK_TOKEN')


def home(request):
    if not request.user.is_authenticated:
        context = {}
        return render(request, 'base.html', context)

    BASE_URL = 'https://api.vk.com/method/'

    method_profile = 'users.get'
    method_friends = 'friends.get'

    url_profile = os.path.join(BASE_URL, method_profile)
    url_friends = os.path.join(BASE_URL, method_friends)

    # получаем id, имя и фамилию пользователя
    data = {
        'access_token': VK_TOKEN,
        'user_ids': request.user.username,
        'v': 5.122,
    }

    try:
        request_profile = requests.post(url_profile, params=data)
        first_name = request_profile.json()['response'][0]['first_name']
        last_name = request_profile.json()['response'][0]['last_name']
        user_id = request_profile.json()['response'][0]['id']
        profile = '{} {}'.format(first_name, last_name)
    except KeyError:
        print('Ошибка при получении данных из JSON-объекта')
    except JSONDecodeError:
        print('Не удалось получить ответ в формате JSON')
    except exceptions.RequestException as e:
        print(f'При попытке соединения возникла следующая ошибка: {e}')

    # получаем имена и фамилии 5 друзей
    data = {
        'user_id': user_id,
        'order': 'random',
        'count': 5,
        'fields': 'nickname',
        'name_case': 'nom',
        'access_token': VK_TOKEN,
        'v': 5.122,
    }
    try:
        request_friends = requests.post(url_friends, params=data)
        friends = request_friends.json().get('response')['items']
        one = '{} {}'.format(friends[0]['first_name'], friends[0]['last_name'])
        two = '{} {}'.format(friends[1]['first_name'], friends[1]['last_name'])
        three = '{} {}'.format(friends[2]['first_name'], friends[2]['last_name'])
        four = '{} {}'.format(friends[3]['first_name'], friends[3]['last_name'])
        five = '{} {}'.format(friends[4]['first_name'], friends[4]['last_name'])
    except KeyError:
        print('Ошибка при получении данных из JSON-объекта')
    except JSONDecodeError:
        print('Не удалось получить ответ в формате JSON')
    except exceptions.RequestException as e:
        print(f'При попытке соединения возникла следующая ошибка: {e}')

    context = {
        'profile': profile,
        'one': one,
        'two': two,
        'three': three,
        'four': four,
        'five': five
    }
    return render(request, 'base.html', context)


def logout(request):
    auth_logout(request)
    return redirect('/')
