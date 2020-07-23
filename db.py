import pymysql
import random
from vk import vk_send
import datetime

TIME = 20

# STATES
#   0 - in DB
#   1 - in search of interlocutor
#   2 - in dialog
#   3 - response to data offer


# connection to db
def get_connection():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='qy.pr.wppw',
                                 db='unichat',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection


# add user_id
def register_in_db(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT user_id FROM registr WHERE user_id = %s"
    cursor.execute(sql, user_id)

    a = 0
    for i in cursor:
        a = i['user_id']

    if a != user_id:

        sql = "INSERT INTO registr(user_id) VALUES (%s)"
        cursor.execute(sql, user_id)
        sql = "INSERT INTO user_info(user_id,user_id_for_sending,start_" \
              "time,state) VALUES(%s,0,SYSDATE(),0)"
        cursor.execute(sql, user_id)

    connection.commit()
    connection.close()


# change column state to "state" for user_id
def change_state(user_id, state):

    connection = get_connection()
    cursor = connection.cursor()

    sql = 'UPDATE user_info SET state = %s WHERE user_id = %s' % (state, user_id)
    cursor.execute(sql)

    connection.commit()
    connection.close()


# update column time with sysdate for user_id
def add_datetime(user_id, time):

    connection = get_connection()
    cursor = connection.cursor()

    sql = 'UPDATE user_info SET %s = SYSDATE() WHERE user_id = %s' % (time, user_id)
    cursor.execute(sql)

    connection.commit()
    connection.close()


# end dialog for user_id
def end_dialog(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    sql = 'UPDATE user_info SET user_id_for_sending = 0 WHERE user_id = %s'
    cursor.execute(sql, user_id)

    connection.commit()
    connection.close()

    change_state(user_id, 0)


# connect user_id and user_id_for_sending
def start_dialog(user_id, user_id_for_sending):

    connection = get_connection()
    cursor = connection.cursor()

    sql = "UPDATE user_info SET user_id_for_sending = %s WHERE user_id = %s" % (user_id_for_sending, user_id)
    cursor.execute(sql)
    sql = "UPDATE user_info SET user_id_for_sending = %s WHERE user_id = %s" % (user_id, user_id_for_sending)
    cursor.execute(sql)

    connection.commit()
    connection.close()

    add_datetime(user_id, "start_time")
    add_datetime(user_id_for_sending, "start_time")

    change_state(user_id, 2)
    change_state(user_id_for_sending, 2)


# get current state for user_id
def get_current_state(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    test = "SELECT state FROM user_info WHERE user_id = %s"
    cursor.execute(test, user_id)
    view = cursor.fetchall()

    connection.commit()
    connection.close()

    # почему только иф? посмотреть позже
    if view != ():

        state = list(view[0].values())[0]

        return state

    else:

        return None


# count how many users are in state 1
def count_in_search():

    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM user_info WHERE state = 1"
    cursor.execute(sql)

    a = 0
    for i in cursor:
        a = i["COUNT(*)"]

    connection.commit()
    connection.close()

    return a


# is user_id in db
def is_in(user_id):

    return get_current_state(user_id) == 0


# is user_id searching
def is_searching(user_id):

    return get_current_state(user_id) == 1


# is user_id connected
def is_connected(user_id):

    return get_current_state(user_id) == 2


# is user_id response
def is_response(user_id):

    return get_current_state(user_id) == 3


# return for user_id
def find_user_id_for_sending(user_id):

    if is_connected(user_id) or is_response(user_id):

        connection = get_connection()
        cursor = connection.cursor()

        sql = "SELECT user_id_for_sending FROM user_info WHERE user_id = %s"
        cursor.execute(sql, user_id)
        view = cursor.fetchall()

        connection.commit()
        connection.close()

        user_id_for_sending = list(view[0].values())[0]

        return user_id_for_sending

    else:

        active = count_in_search()

        if active > 1:

            connection = get_connection()
            cursor = connection.cursor()

            user_send = random.randrange(1, active)

            sql = "SELECT user_id FROM registr WHERE user_id != %s"
            cursor.execute(sql, user_id)
            view = cursor.fetchall()

            connection.commit()
            connection.close()

            user_id_for_sending = list(view[user_send-1].values())[0]

            return user_id_for_sending

        else:

            return None


# connect all users, who is searching for dialog
def searching_for_dialog():

    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT user_id FROM user_info WHERE state = 1"
    cursor.execute(sql)
    view = cursor.fetchall()
    print(view)

    while count_in_search() > 1:

        print(view)

        user_id = list(view[0].values())[0]
        user_id_for_sending = find_user_id_for_sending(user_id)
        start_dialog(user_id, user_id_for_sending)

        vk_send(user_id, 'Собеседник был найден', 2)
        vk_send(user_id_for_sending, 'Собеседник был найден', 2)

        sql = "SELECT user_id FROM user_info WHERE state = 1"
        cursor.execute(sql)
        view = cursor.fetchall()


# change state to 3 for all users, which start_time is more than 10 min
def check_start_time():

    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM user_info WHERE state = 2"
    cursor.execute(sql)
    view = cursor.fetchall()

    connection.commit()
    connection.close()

    for i in view:

        timing = (datetime.datetime.now() - i['start_time']).total_seconds()

        if timing > TIME:

            vk_send(i['user_id'], 'Время диалога истекло. Желаете ли вы продолжить общение?', 3)
            change_state(i['user_id'], 3)













