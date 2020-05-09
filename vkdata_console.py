import requests
import json

url = 'https://sas.alpeconsulting.ru/vkactivity/data'


def get(url):
    response = requests.get(url)
    for el in response.json():
        print("id:", str(el['id']) + ";", el['name'], el['surname'] + ",", el['date'] + ";", "Активность:",
              el['activity'])


def get_id(url):
    input_id = input('Id: ')
    data = (requests.get(url + '/' + input_id)).json()
    print("id:", str(data['id']) + ";", data['name'], data['surname'] + ",", data['date'] + ";", "Активность:",
          data['activity'])


def post(url):
    isdone = False
    while not isdone:
        try:
            name = input('Имя: ')
            surname = input('Фамилия:')
            bdate = input('Дата рождения (xx.yy.zzzz): ')
            activity = int(input('Активность: '))

            requests.post(url,
                          json={'name': name,
                                'surname': surname,
                                'date': bdate,
                                'activity': activity})
            isdone = True
        except:
            print("Не удалось добавить запись")

    if isdone:
        print('Запись добавлена')


def delete(url):
    print('Вы уверены, что хотите удалить все записи(1 - да, 2 - нет)')
    choice_delete = int(input('Ответ: '))
    if choice_delete == 1:
        requests.delete(url)
        print('Все записи удалены')
    elif choice_delete == 2:
        print('Записи не удалены')
    else:
        print('Такого варианта ответа нет')
        delete(url)


def delete_id(url):
    input_id = input('Id: ')
    print('Вы уверены, что хотите удалить запись(1 - да, 2 - нет)')
    choice_delete_id = int(input('Ответ: '))
    if choice_delete_id == 1:
        requests.delete(url + '/' + input_id)
        print('Запись удалена')
    elif choice_delete_id == 2:
        print('Запись не удалена')
    else:
        print('Такого варианта ответа нет')
        delete_id(url)


def exit_choice():
    print('Действия: ')
    print('new - новое действие')
    print('exit - выйти')
    print()
    input_answ = input('Выбор: ')
    if input_answ == 'new':
        choice()
    elif input_answ == 'exit':
        exit()
    else:
        print('Такого варианта ответа нет')
        print()
        exit_choice()


def choice():
    print('Действия:')
    print('get - получить все записи')
    print('get id - получить конкретную запись')
    print('post - доавить запись')
    print('delete - удалить все записи')
    print('delete id - удалить конкретную запись')
    print()
    answer = input("Выбор: ")

    if answer == 'get':
        get(url)
    elif answer == 'get id':
        get_id(url)
    elif answer == 'post':
        post(url)
    elif answer == 'delete':
        delete(url)
    elif answer == 'delete id':
        delete_id(url)
    elif answer == 'new':
        print()
        choice()
    else:
        print('Такого варианта ответа нет')
        choice()
    print()
    exit_choice()


choice()


