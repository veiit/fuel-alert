#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Communication.TelegramHandler.Telegram import TelegramBot
from DataHandler.SQLHandler.SQLHandler import SQLHandler
from Utils.Time import getTimestamp


class Messenger:

    def __init__(self):
        self.TelegramBot = TelegramBot()
        self.SQLHandler = SQLHandler()


    def sendMsg(self, winning_gas_station, best_price):
        alert_price = best_price
        alert_sent = getTimestamp()

        # build Msg Text
        msg_text = self.buildMsgText(winning_gas_station, best_price)

        # send Msg with Telegramm
        print(f'[{getTimestamp()}][Messenger] try sending Msg')
        msg_was_sent = self.TelegramBot.sendMsg(msg_text)

        if not msg_was_sent:
            return False

        # update stats
        self.updateAlertStatistics(alert_price, alert_sent)
        print(f'[{getTimestamp()}][Messenger] Message sent at: {alert_sent} [{alert_price}]')

        return True


    def buildMsgText(self, winning_gas_station, bestprice):
        gas_station_id, price, name, isOpen, time_stamp, gas_type, distance = winning_gas_station
        name, brand, street, houseNr, postCode, city = self.SQLHandler.returnGasStationDetailsFromId(gas_station_id)

        time_ = time_stamp.split(" ")[1]
        name = name[:20]
        address = f"{street} {houseNr}, {postCode} {city}"

        msg_text = f"Neuer Bestpreis: {bestprice}€ [{gas_type}]\n"
        msg_text += f"um {time_}\n"
        msg_text += f"\n"
        msg_text += f"{name}\n"
        msg_text += f"{address}\n"
        msg_text += f"Distance: {distance:.2f} km"

        return msg_text

    def updateAlertStatistics(self, alert_price, time_stamp):
        was_successful = self.SQLHandler.updateStatisticValue("last_alert_price", alert_price)
        was_successful = self.SQLHandler.updateStatisticValue("last_alert_price_time_stamp", time_stamp)

