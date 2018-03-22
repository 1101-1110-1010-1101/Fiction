import vk_api
import time
import random
import datetime

api_token = '86d5839b2eddcd58817430ed61803372e322e5dd5fb28196bcd7c2bad9a59a58249241b62453f91fea5dc'
print('Fiction initialized')
vk = vk_api.VkApi(token=api_token)
print('Connecting...')
vk._auth_token()
print('Connected successfully!\nFiction is running')

values = {'out':0, 'count':100, 'time_offset':10}
response = vk.method('messages.get', values)
answers = ['Да', 'Нет', 'Тебе бы это понравилось, ', '', 'Не смеши грибочки', '...', 'Копенгаген. А ты чего ожидала?',
           'Не расстраивайся по этому поводу - лучше напиши фанфик',
           'Следуй за ветром', 'Возможно, в следующей жизни', 'Отнюдь!']
id_name = {}


def fetch_user(user_id):
    name = id_name.get(user_id)
    if name is None:
        id_name[user_id] = vk.method('users.get', {'user_id': user_id})[0]['first_name']
        print(id_name[user_id])
    return id_name[user_id]


def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        print('Got message from ' + str(vk.method('users.get', {'user_id': item['user_id']})) + str(datetime.datetime.now()))
        if response['items'][0]['body'] == 'Кто ты?':
            write_msg(item['user_id'], 'Я Фикшн, приятно познакомиться, ' + fetch_user(item['user_id']))
        elif response['items'][0]['body'] == 'О, всевышний!':
            write_msg(item['user_id'], 'Задай свой вопрос, смертный')
            while True:
                response = vk.method('messages.get', values)
                if response['items']:
                    values['last_message_id'] = response['items'][0]['id']
                    r = random.randrange(0, 11, 1)
                    if r == 2:
                        write_msg(item['user_id'], answers[r] + fetch_user(item['user_id']))
                        break
                    elif r == 3:
                        write_msg(item['user_id'], 'Нет, ' + fetch_user(item['user_id'])
                                  + ', твоё финансовое положение этого не позволяет')
                        break
                    else:
                        write_msg(item['user_id'], answers[r])
                        break
        else:
            write_msg(item['user_id'], 'Я не понимаю тебя')

    time.sleep(1)
