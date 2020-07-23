import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


token = "130238bd599aabd7f8d252debd4ee41eb7d05507929b4d744cc3a1eafc6f98e27d4342c58ebabd0e87c26"
group_id = '195460898'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=group_id)


# return name of button
def get_button(mode):

    if mode == 0:

        return 'keyboard\start.json'

    elif mode == 1:

        return 'keyboard\ew.json'

    elif mode == 2:

        return 'keyboard\dialog.json'

    elif mode == 3:

        return 'keyboard\swer.json'

    else:

        return 'keyboard\default.json'


# send message to user_id in vk with button mode
def vk_send(user_id, message, mode):

    keyboard = get_button(mode)

    if message == ' ':

        vk.messages.send(peer_id=user_id,
                         random_id=get_random_id(),
                         keyboard=open(keyboard, "r", encoding="UTF-8").read())

    else:

        vk.messages.send(peer_id=user_id,
                         message=message,
                         random_id=get_random_id(),
                         keyboard=open(keyboard, "r", encoding="UTF-8").read())