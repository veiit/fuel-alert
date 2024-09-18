#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.config import BEST_PRICE_PERIOD_LENGTH
from DataHandler.SQLHandler.SQLHandler import SQLHandler


class BestPriceCurrentPeriod:

    def __init__(self):
        self.BEST_PRICE_PERIOD_LENGTH = BEST_PRICE_PERIOD_LENGTH

        self.SQLHandler = SQLHandler()


    def run(self):

        time_stamp_and_prices = self.getBestPricesFromDB()
        if time_stamp_and_prices == []:
            return False

        min_price, time_stamp_youngest = self.buildStatisic(time_stamp_and_prices)

        update_was_successful = self.updateDBMinPrice(min_price)
        if not update_was_successful:
            return False

        update_was_successful = self.updateDBMinPriceTS(time_stamp_youngest)
        return update_was_successful


    def getBestPricesFromDB(self):
        time_stamp_and_price = self.SQLHandler.returnBestPricesInLastXDays(
            x=self.BEST_PRICE_PERIOD_LENGTH)  # BEST_PRICE_PERIOD_LENGTH = 14
        return time_stamp_and_price


    def buildStatisic(self, time_stamp_and_prices):
        prices = [i[1] for i in time_stamp_and_prices]
        min_price = min(prices)

        time_stamps = [i[0] for i in time_stamp_and_prices if i[1] == min_price]
        time_stamp_youngest = max(time_stamps)

        return min_price, time_stamp_youngest


    def updateDBMinPrice(self, min_price):
        was_successful = self.SQLHandler.updateStatisticValue("best_price_last_period", min_price)
        return was_successful


    def updateDBMinPriceTS(self, time_stamp_youngest):
        was_successful = self.SQLHandler.updateStatisticValue("best_price_last_period_time_stamp", time_stamp_youngest)
        return was_successful