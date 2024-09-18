#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.Time import getTimestamp, isTimestampOlderThenXdays

from DataHandler.SQLHandler.SQLHandler import SQLHandler
from config.config import BEST_PRICE_PERIOD_LENGTH


class AlertingLogic:

    def __init__(self):
        self.SQLHandler = SQLHandler()


    def ckeckForAlert(self):
        ''' only alert if:
        - a new best prices was reached in the current period AND
        - the last prices that was send ist higher or was send outside of the current period

        '''

        alert_stats_relevant = self.getAlertStatus()
        if not alert_stats_relevant:
            return False

        new_best_price_exists = self.checkIfNewBestPriceExists()
        if not new_best_price_exists:
            return False

        return True


    def getAlertStatus(self):
        last_alert_price = self.SQLHandler.returnStatisticValue("last_alert_price")
        alert_price_time_stamp = self.SQLHandler.returnStatisticValue("last_alert_price_time_stamp")
        current_best_price = self.SQLHandler.returnStatisticValue("current_best_price")

        last_alert_is_outside_period = isTimestampOlderThenXdays(alert_price_time_stamp, BEST_PRICE_PERIOD_LENGTH)

        # if the last communicated price is outside the current period, ignore the last communicated price
        if last_alert_is_outside_period:
            return True

        # if the current_best_price was already communicated in the current period, then dont do it again
        if float(last_alert_price) > float(current_best_price):
            return True

        return False



    def checkIfNewBestPriceExists(self):
        best_price_last_period = self.SQLHandler.returnStatisticValue("best_price_last_period")
        best_price_last_period_time_stamp = self.SQLHandler.returnStatisticValue("best_price_last_period_time_stamp")
        current_best_price = self.SQLHandler.returnStatisticValue("current_best_price")
        current_best_price_time_stamp = self.SQLHandler.returnStatisticValue("current_best_price_time_stamp")

        if best_price_last_period == None or current_best_price == None:
            print(f'[{getTimestamp()}][Logic][ERROR] best_price_last_period: "{best_price_last_period}", current_best_price: "{current_best_price}"')
            return False

        if best_price_last_period_time_stamp == current_best_price_time_stamp:
            return True

        if float(best_price_last_period) > float(current_best_price):
            return True

        return False
