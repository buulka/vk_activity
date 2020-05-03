import vk
import time
import datetime
import colorama
from prettytable import PrettyTable
from colorama import Fore
from colorama import Style
colorama.init()

vkapi = None


class Color:
    Cyan = '\033[96m'
    END = '\033[0m'
    Blue = '\033[94m'


print(Color.Cyan + "Авторизация" + Color.END)

while True:
    try:
        print("Введите логин: ", end="")
        login = input()
        print("Введите пароль: ", end="")
        password = input()
        session = vk.AuthSession(app_id='2685278', user_login=login, user_password=password)
        vkapi = vk.API(session, v="5.103")
        break
    except:
        print(f'Ошибка! Попробуйте снова')

friends_count = vkapi.friends.get(order='hints')['count']
groups_count = vkapi.groups.get()['count']
faves_count = vkapi.fave.get()['count']
photos_count = vkapi.photos.getAll()['count']
posts_count = vkapi.wall.get()['count']

bestfriends = vkapi.friends.get(order='hints', count='5')
now = datetime.datetime.now()

coef = 0

print()

if groups_count < 50:
    groups_coef = 3
elif 50 < groups_count < 250:
    groups_coef = 5
elif 250 <= groups_count < 500:
    groups_coef = 7
elif 500 <= groups_count < 750:
    groups_coef = 10
elif 750 <= groups_count < 1000:
    groups_coef = 12
else:
    groups_coef = 15

coef += groups_coef

if friends_count < 50:
    friends_coef = 5
elif 50 < friends_count < 250:
    friends_coef = 10
elif 250 <= friends_count < 500:
    friends_coef = 15
elif 500 <= friends_count < 750:
    friends_coef = 20
elif 750 <= friends_count < 1000:
    friends_coef = 25
else:
    friends_coef = 30

coef += friends_coef

if photos_count < 50:
    photos_coef = 1
elif photos_count >= 50:
    photos_coef = 3
elif photos_count >= 500:
    photos_coef = 5

coef += photos_coef

if posts_count < 10:
    posts_coef = 1
elif 10 <= posts_count < 50:
    posts_coef = 2
elif posts_count >= 50:
    posts_coef = 3

coef += posts_coef

if faves_count < 25:
    faves_coef = 0.5
elif 20 <= faves_count <= 50:
    faves_coef = 1
else:
    faves_coef = 1.5

coef += faves_coef

days_coef = 0

print(f'Загрузка', end="")

for i in range(len(bestfriends['items'])):
    try:
        msg = vkapi.messages.getHistory(user_id=bestfriends['items'][i], offset='200', count='1')
        date = msg['items'][0]['date']
        days = (now - datetime.datetime.fromtimestamp(date)).days
        if days <= 2:
            days_coef += 10
        elif 2 < days < 10:
            days_coef += 6
        elif 10 <= days < 15:
            days_coef += 2
        else:
            days_coef += 1
            print(f'.', end="")
        time.sleep(2)
    except:
        pass

coef += days_coef
print()

th = [Color.Cyan + "Критерий" + Color.END, Color.Cyan + "Баллы" + Color.END]
td = ['Группы', groups_coef,
      'Друзья', friends_coef,
      'Фото', photos_coef,
      'Посты', posts_coef,
      'Закладки', faves_coef,
      'Сообщения', days_coef]
columns = len(th)
table = PrettyTable(th)
td_data = td[:]

while td_data:
    table.add_row(td_data[:columns])
    td_data = td_data[columns:]
table_print = table
print(table_print)

# TEST COMMIT

print()
print(Color.Cyan + "Итого: " + Color.END, coef)
print()
input("Нажмите Enter для выхода")
