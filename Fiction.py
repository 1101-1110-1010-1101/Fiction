import vk_api
import time
import random
import datetime
import markovify

api_token = '86d5839b2eddcd58817430ed61803372e322e5dd5fb28196bcd7c2bad9a59a58249241b62453f91fea5dc'
print('Fiction initialized')
vk = vk_api.VkApi(token=api_token)
print('Connecting...')
vk._auth_token()
print('Connected successfully!\nFiction is running')
date_n = str(datetime.datetime.today().date())
log_file = open('C:\\Users\\User\\Desktop\\Проекты\\Fiction\\logs\\' + str(date_n) + ".log", 'a')
log_file.write('Initialized at ' + str(datetime.datetime.now().time()) + '\n')

values = {'out':0, 'count':100, 'time_offset':10}
response = vk.method('messages.get', values)
answers = ['Да', 'Нет', 'Тебе бы это понравилось, ', '', 'Не смеши грибочки', '...', 'Копенгаген. А ты чего ожидала?',
           'Не расстраивайся по этому поводу - лучше напиши фанфик',
           'Следуй за ветром', 'Возможно, в следующей жизни', 'Отнюдь!']
id_name = {}
stats = {}


def fetch_user(user_id):
    name = id_name.get(user_id)
    if name is None:
        id_name[user_id] = vk.method('users.get', {'user_id': user_id})[0]['first_name']
    return id_name[user_id]


def count_msgs(user_id):
    id = stats.get(user_id)
    if id is None:
        stats[user_id] = 1
    else:
        stats[user_id] += 1


def show_stats():
    result = ''
    for i in stats.keys():
        result += vk.method('users.get', {'user_id': i})[0]['first_name'] + ' ' +\
                  vk.method('users.get', {'user_id': i})[0]['last_name'] + ': ' +\
                  str(stats.get(i) - 1) + '\n'
    return result


def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


def get_markov_chain():
    with open('C:\\Users\\User\\Desktop\\ITMO\\source.txt') as f:
        text = f.read()
    return markovify.Text(text)


text = get_markov_chain()

while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        fetch_user(item['user_id'])
        print('Got message from ' + str(vk.method('users.get', {'user_id': item['user_id']})) + str(datetime.datetime.now()))
        count_msgs(item['user_id'])
        log_file.write(('Got message from ' + str(vk.method('users.get', {'user_id': item['user_id']})) + str(datetime.datetime.now()) + '\n'))
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
        elif response['items'][0]['body'] == 'Расскажи историю':
            crime_and_punishment = ''
            for i in range(5):
                a = 'None '
                while a == 'None ':
                    a = str(text.make_sentence()) + ' '
                crime_and_punishment += a
            write_msg(item['user_id'], crime_and_punishment)
        elif response['items'][0]['body'] == '\\fic.save_log':
            if item['user_id'] == 155703829:
                log_file.close()
                log_file = open('C:\\Users\\User\\Desktop\\Проекты\\Fiction\\logs\\' + str(date_n) + ".log", 'a')
            else:
                write_msg(item['user_id'], 'Извините, не хватает прав для выполнения команды')
        elif response['items'][0]['body'] == '\\fic.exit':
            if item['user_id'] == 155703829:
                write_msg(item['user_id'], 'До встречи, ' + fetch_user(item['user_id']))
                log_file.close()
                exit(0)
            else:
                write_msg(item['user_id'], 'Извините, не хватает прав для выполнения команды')
        elif response['items'][0]['body'] == '\\fic.stats':
            write_msg(item['user_id'], show_stats())
        else:
            write_msg(item['user_id'], 'Я не понимаю тебя')

    time.sleep(1)
