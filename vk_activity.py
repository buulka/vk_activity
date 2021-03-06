import vk
import time
import datetime
import PySimpleGUI as sg
import requests


def get_groups_coef(groups_count):
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

    return groups_coef


def get_friends_coef(friends_count):
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

    return friends_coef


def get_photos_coef(photos_count):
    photos_coef = 0
    if photos_count < 50:
        photos_coef = 1
    elif photos_count >= 50:
        photos_coef = 3
    elif photos_count >= 500:
        photos_coef = 5

    return photos_coef


def get_posts_coef(posts_count):
    posts_coef = 0
    if posts_count < 10:
        posts_coef = 1
    elif 10 <= posts_count < 50:
        posts_coef = 2
    elif posts_count >= 50:
        posts_coef = 3

    return posts_coef


def get_faves_coef(faves_count):
    if faves_count < 25:
        faves_coef = 0.5
    elif 20 <= faves_count <= 50:
        faves_coef = 1
    else:
        faves_coef = 1.5

    return faves_coef


def get_messages_coef(bestfriends):
    now = datetime.datetime.now()
    days_coef = 0
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
            time.sleep(2)
        except:
            pass

    return days_coef


sg.theme('LightGrey1')

layout_auth = [[sg.Text('Авторизация ВК', pad=(55, 10), font=('Verdana', '15'))],
               [sg.Text('Логин:  '), sg.InputText(size=(30, 1))],
               [sg.Text('Пароль:'), sg.InputText(size=(30, 1), do_not_clear=False, password_char='*')],
               [sg.OK('Вход', size=(10, 2), pad=(95, 30))]]

window_auth = sg.Window('Активность в ВК', layout_auth, size=(300, 200))

layout_result = [[sg.Text('Баллы', pad=(100, 5), font=('Verdana', '15'))],
                 [sg.Text('Группы:', size=(11, 1)), sg.Text(size=(15, 1), key='-GROUPS-')],
                 [sg.Text('Друзья:', size=(11, 1)), sg.Text(size=(15, 1), key='-FRIENDS-')],
                 [sg.Text('Фото:', size=(11, 1)), sg.Text(size=(15, 1), key='-PHOTOS-')],
                 [sg.Text('Посты:', size=(11, 1)), sg.Text(size=(15, 1), key='-POSTS-')],
                 [sg.Text('Закладки:', size=(11, 1)), sg.Text(size=(15, 1), key='-FAVES-')],
                 [sg.Text('Сообщения:', size=(11, 1)), sg.Text(size=(15, 1), key='-MESSAGES-')],
                 [sg.Text()],
                 [sg.Text('Общий коэффициент активности: '), sg.Text(size=(15, 1), key='-OUTPUT-')],
                 [sg.Submit('Отправить результат на сервер', size=(20, 2), pad=(65, 30), key='-SUBMIT-')]]

while True:
    event, values = window_auth.read()
    if event == 'Вход':
        success = True
        coef = 0
        vkapi = None

        try:
            login = values[0]
            password = values[1]
            if login == '' or password == '':
                raise AssertionError

            session = vk.AuthSession(app_id='2685278', user_login=login, user_password=password)
            vkapi = vk.API(session, v="5.103")

        except:
            success = False
            sg.popup_annoying('Введены неверные данные', non_blocking=False, background_color='lightgray')

        if success:
            window_auth.close()

            window_result = sg.Window('Результат', layout_result, size=(300, 360))
            window_result.Finalize()

            window_result['-SUBMIT-'].update(disabled=True)
            window_result.Refresh()

            groups_count = vkapi.groups.get()['count']
            groups_coef = get_groups_coef(groups_count)
            window_result['-GROUPS-'].update(groups_coef)
            window_result.Refresh()

            friends_count = vkapi.friends.get(order='hints')['count']
            friends_coef = get_friends_coef(friends_count)
            window_result['-FRIENDS-'].update(friends_coef)
            window_result.Refresh()

            photos_count = vkapi.photos.getAll()['count']
            photos_coef = get_photos_coef(photos_count)
            window_result['-PHOTOS-'].update(photos_coef)
            window_result.Refresh()

            posts_count = vkapi.wall.get()['count']
            posts_coef = get_posts_coef(posts_count)
            window_result['-POSTS-'].update(posts_coef)
            window_result.Refresh()

            faves_count = vkapi.fave.get()['count']
            faves_coef = get_faves_coef(faves_count)
            window_result['-FAVES-'].update(faves_coef)
            window_result.Refresh()

            window_result['-MESSAGES-'].update('Загрузка...')

            window_result.Refresh()
            bestfriends = vkapi.friends.get(order='hints', count='5')
            messages_coef = get_messages_coef(bestfriends)
            window_result['-MESSAGES-'].update(messages_coef)
            window_result.Refresh()

            coef = groups_coef + posts_coef + messages_coef + faves_coef + friends_coef + photos_coef

            window_result['-OUTPUT-'].update(coef)

            window_result['-SUBMIT-'].update(disabled=False)
            window_result.Refresh()

            users_firstname = vkapi.account.getProfileInfo()['first_name']
            users_lastname = vkapi.account.getProfileInfo()['last_name']
            users_bdate = vkapi.account.getProfileInfo()['bdate']

            while True:
                event, values = window_result.read()
                if event == '-SUBMIT-':
                    try:
                        response = requests.post('https://sas.alpeconsulting.ru/vkactivity/data',
                                                 json={'name': users_firstname,
                                                       'surname': users_lastname,
                                                       'date': users_bdate,
                                                       'activity': coef})

                        window_result['-SUBMIT-'].update(disabled=True)
                        window_result.Refresh()
                    except:
                        sg.popup_annoying('Не удалось отправить данные', non_blocking=False,
                                          background_color='lightgray')
                elif event is None:
                    window_result.close()
                    break

    if event is None:
        window_auth.close()
        break
