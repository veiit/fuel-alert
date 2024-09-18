#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.Time import getTimestamp

from DataHandler.DataHandler import DataHandler
from Logic.Alerting import AlertingLogic
from Logic.GasstationPicker import GasStationPicker
from Communication.Messenger import Messenger

class FuelAlert:
    '''
    This service informs (via TelegramBot) if a new low fuel prices was reached in a given time period (e.g. last 3 weeks).

    The service uses the fuel prices from the following API https://creativecommons.tankerkoenig.de/
    '''



    def __init__(self):
        self.DataHandler = DataHandler()
        self.AlertingLogic = AlertingLogic()
        self.GasStationPicker = GasStationPicker()
        self.Messenger = Messenger()


    def run(self):
        print(f"\n[{getTimestamp()}][FuelAlert] Request new fuel prices")
        # request and save new data
        was_successful, cheapest_gas_stations = self.DataHandler.run()
        if not was_successful:
            return False

        print(f"[{getTimestamp()}][FuelAlert] New fuel prices received and processed")

        # check if an alert should be raised
        send_alert = self.AlertingLogic.ckeckForAlert()

        if not send_alert:
            print(f"[{getTimestamp()}][FuelAlert] No new best price found")
            return False

        # get the gas station with the best price
        # if there is more then one, get the closest
        winning_gas_station, new_best_price = self.GasStationPicker.pickWinningGasStation(cheapest_gas_stations)

        # send alert
        self.Messenger.sendMsg(winning_gas_station, new_best_price)
        print(f'[{getTimestamp()}][FuelAlert] New best price: {new_best_price}')









if __name__ == "__main__":
    FuelAlertService = FuelAlert()
    FuelAlertService.run()
