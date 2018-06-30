import vk_api
import time
import random
import datetime
import markovify
import re


class methods:
    def greet(item):
        write_msg(item['user_id'], greetings[random.randrange(0, len(greetings), 1) + fetch_user(item['user_id'])])

character = open('C:\\Users\\User\\Desktop\\Проекты\\Fiction\\Character.txt', 'r')
char_list = character.readline().split(',')
eyes_list = character.readline().split(',')
eyebrows_list = character.readline().split(',')
lob_list = character.readline().split(',')
gaze_list = character.readline().split(',')
nose_list = character.readline().split(',')
hair_list = character.readline().split(',')
figure_list = character.readline().split(',')
walking_list = character.readline().split(',')
names_list = character.readline().split(',')


class Personage(object):
    def __init__(self):
        self.main_characteristic = char_list[random.randrange(0, len(char_list), 1)]
        self.secondary_characteristic = char_list[random.randrange(0, len(char_list), 1)]
        self.eyes = eyes_list[random.randrange(0, len(eyes_list), 1)]
        self.eyebrows = eyebrows_list[random.randrange(0, len(eyebrows_list), 1)]
        self.lob = lob_list[random.randrange(0, len(lob_list), 1)]
        self.gaze = gaze_list[random.randrange(0, len(gaze_list), 1)]
        self.nose = nose_list[random.randrange(0, len(nose_list), 1)]
        self.hair = hair_list[random.randrange(0, len(hair_list), 1)]
        self.figure = figure_list[random.randrange(0, len(figure_list), 1)]
        self.walking = walking_list[random.randrange(0, len(walking_list), 1)]
        self.name = names_list[random.randrange(0, len(names_list), 1)]

    def toString(self):
        return self.name + '\nОсновная черта - ' + self.main_characteristic + '\nВторичная - ' + self.secondary_characteristic + '\nГлаза - ' + self.eyes + ', ' + self.eyebrows + ' брови, ' + self.lob + ' лоб' + ', взгляд - ' + self.gaze + ', ' + self.nose + ' нос, ' + self.hair + ' волосы, ' + self.figure + ' фигура, походка - ' + self.walking


api_token = '***'
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
greetings = ['Привет, ', 'Здравствуй, ', 'Рад снова видеть тебя, ']



patterns = []
decoder = {r'.*привет.*': 'greet'}
for k in decoder.keys():
    patterns.append(re.compile(k))

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


def decodeMessage(item):
    for patrn in patterns:
        matches = patrn.findall(item['body'])
        if len(matches) != 0:
            funk = getattr(methods, decoder[patrn.pattern])
            funk(item)
        else: print('Youre y****n, Vanya')

text = get_markov_chain()
pers = Personage()
print(json.dumps(pers))


while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        fetch_user(item['user_id'])
        decodeMessage(item)
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

        elif response['items'][0]['body'] == '\\fic.exit':
            if item['user_id'] == 155703829:
                write_msg(item['user_id'], 'До встречи, ' + fetch_user(item['user_id']))
                log_file.close()
                exit(0)
            else:
                write_msg(item['user_id'], 'Извините, не хватает прав для выполнения команды')
        elif response['items'][0]['body'] == '\\fic.stats':
            write_msg(item['user_id'], show_stats())
        elif response['items'][0]['body'] == 'Давай генерить персов':
           test = Personage()
           write_msg(item['user_id'], test.toString())
        elif response['items'][0]['body'] == 'Two Boats':
            write_msg(item['user_id'], 'Хмм, а ты неплох!\n1100 0000 1111 1111 1110 1110')
        elif response['items'][0]['body'] == 'C0FFEE':
            write_msg(item['user_id'], 'Так держать! Введите код доступа (морзянка)')
        else:
            write_msg(item['user_id'], 'Я не понимаю тебя')

    time.sleep(1)


