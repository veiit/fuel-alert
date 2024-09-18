#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json

from Utils.Time import getTimestamp
from config.config import TELEGRAMDATA

class TelegramBot:

    def __init__(self):
        token = TELEGRAMDATA["token"]
        self.APIpath = f"https://api.telegram.org/bot{token}"
        self.__USERID = TELEGRAMDATA["ID"] # The message will only be send to this Telegram ID


    def sendMsg(self, msg_text):

        userid = self.__ID
        url = f"{self.APIpath}/sendMessage?chat_id={userid}&text={msg_text}"

        response = requests.get(url)
        html_status = str(response.status_code)

        if html_status != "200":
            content = json.loads(response.text)
            print(f'[{getTimestamp()}][TelegramBot][ERROR] Sending failed: {html_status} - {content["description"]}')
            return False

        return True



