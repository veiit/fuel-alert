#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.Time import getTimestamp


from DataHandler.APIHandler.TankerkoenigAPI import TankerkoenigAPI
from DataHandler.APIResponceTransformer.DataTransformer import DataTransformer
from DataHandler.SQLHandler.SQLHandler import SQLHandler

from DataHandler.GasStationDetails.UpdateHandler import UpdateHandler
from DataHandler.StatisticsGenerator.BestPriceCurrentPeriod import BestPriceCurrentPeriod

class DataHandler:
    '''
    This Class:
    - requests the gas station data from the Tankerkoenig API -> https://creativecommons.tankerkoenig.de/
    - filters and enriches the data
    - saves the data to sqlite db
    - creates statistics from the saved data and updates them in the db
    '''



    def __init__(self):
        self.TK_API = TankerkoenigAPI()
        self.DataTransformer = DataTransformer()
        self.SQLDB = SQLHandler()

        self.UpdateGasStationDetailsHandler = UpdateHandler()
        self.BestPriceCurrentPeriod = BestPriceCurrentPeriod()



    def run(self):
        request_was_successful, cheapest_gas_stations, gas_station_details_dict = self.requestNewGasStationData()

        if not request_was_successful:
            print(f"[{getTimestamp()}][DataHandler] Data could not be requested")
            return False, []

        db_update_was_successful = self.saveNewGasStationPrices(cheapest_gas_stations)
        if not db_update_was_successful:
            print(f"[{getTimestamp()}][DataHandler] New prices could not be saved to db")
            return False, []

        # save best price
        save_was_successful, best_price = self.saveNewBestFuelPrice(cheapest_gas_stations)

        if not save_was_successful:
            print(f"[{getTimestamp()}][DataHandler] best price could not be saved to DB")
            return False, []

        # If new gas stations where in API response, save the new gas station detail as well in db
        self.UpdateGasStationDetailsHandler.run(cheapest_gas_stations, gas_station_details_dict)


        # build statisic
        statisticbuild_was_successful = self.BestPriceCurrentPeriod.run()
        if not statisticbuild_was_successful:
            print(f"[{getTimestamp()}][DataHandler] Statistics could not be updated")
            return False, []

        # delete aus best_price_history  > 90 days
        # TODO

        return True, cheapest_gas_stations


    def requestNewGasStationData(self):
        # Request new Data from API
        request_was_successful, html_status, list_of_gas_stations, time_stamp = self.TK_API.requestChosenGasStations()
        if not request_was_successful:
            return False, [], []

        # Normalize the Data
        cheapest_gas_stations, gas_station_details_dict = self.DataTransformer.run(list_of_gas_stations, time_stamp)

        return True, cheapest_gas_stations, gas_station_details_dict



    def saveNewGasStationPrices(self, cheapest_gas_stations):
        # Save Data to DB
        data_was_added_to_DB = self.SQLDB.addNewStationPrices(cheapest_gas_stations)
        if not data_was_added_to_DB:
            return False

        return True


    def saveNewBestFuelPrice(self, best_price_and_time_stamp):
        best_price = best_price_and_time_stamp[0][1]
        time_stamp_of_request = best_price_and_time_stamp[0][4]

        data_was_added_to_DB = self.SQLDB.addNewBestPrice(best_price, time_stamp_of_request)
        if not data_was_added_to_DB:
            return False, None

        update_was_successful = self.SQLDB.updateStatisticValue("current_best_price", best_price)
        update_was_successful = self.SQLDB.updateStatisticValue("current_best_price_time_stamp", time_stamp_of_request)

        return True, best_price



