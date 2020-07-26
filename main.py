from db import Database
from vk import *
from config import init_config
import pymysql
letter = 'configs/letter.txt'


try:
    config = init_config().get_settings()
    db = Database(config)

except pymysql.err.OperationalError:
    print('Не удаётся подключиться к БД')
    quit()


while True:

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:

            if event.from_user:

                user_id = event.object.message['peer_id']
                message = event.message['text']
                db.save_message(user_id, message)

                if message.lower() == 'кто тебя создал?':

                    response = 'vk.com/id116895282 и vk.com/id209646771'
                    vk_send(user_id, response, -1)

                if db.is_connected(user_id):

                    user_id_for_sending = db.find_user_id_for_sending(user_id)

                    if message.lower() == "отправить свои контакты":

                        response = 'Ваш собеседник хочет продолжить общение. vk.com/id' + str(user_id)
                        vk_send(user_id_for_sending, response, 1)
                        vk_send(user_id, 'Сообщение было отправлено', 1)
                        db.end_dialog(user_id)

                    if message.lower() == 'прекратить общение':

                        response = 'Ваш собеседник не захотел общаться с вами'

                        mode = 0

                        if db.is_response(user_id):

                            mode = 3

                        if db.is_connected(user_id) or db.is_connected(user_id):

                            mode = 1

                        vk_send(user_id_for_sending, response, mode)
                        vk_send(user_id, 'Диалог окончен', 1)
                        db.end_dialog(user_id)
                        db.end_dialog(user_id_for_sending)

                    else:

                        vk_send(user_id_for_sending, message, 2)

                elif db.is_in(user_id) and message.lower() == 'найти собеседника':

                    db.change_state(user_id, 1)

                elif db.is_response(user_id):

                    user_id_for_sending = db.find_user_id_for_sending(user_id)

                    if message.lower() == 'да':

                        response = 'Ваш собеседник хочет продолжить общение. vk.com/id'+str(user_id)
                        vk_send(user_id_for_sending, response, 1)
                        vk_send(user_id, 'Сообщение было отправлено', 1)
                        db.end_dialog(user_id)

                    if message.lower() == 'нет':

                        response = 'Ваш собеседник отказался продолжить общение с вами'
                        vk_send(user_id_for_sending, response, 1)
                        vk_send(user_id, 'Сообщение было отправлено', 1)
                        db.end_dialog(user_id)

                elif message.lower() == 'начать новый диалог' and not db.is_in(user_id):

                    response = 'Вы были добавлены в список'
                    db.register_in_db(user_id)
                    vk_send(user_id, response, 1)

            db.searching_for_dialog()

            db.check_start_time()

        elif event.type == VkBotEventType.GROUP_JOIN:

            user_id = event.obj.user_id
            message = open(letter, "r", encoding="UTF-8").read()
            vk_send(user_id, message, 0)
