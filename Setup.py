#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.config import ROOT_DB
from DataHandler.SQLHandler.SQLHandler import SQLHandler
from Utils.GeocoordConverter import PLZtoGeoCoordConverter

class Setup:

    def __init__(self):

        self.SQLHandler = SQLHandler()
        self.PLZtoGeoCoordConverter = PLZtoGeoCoordConverter()


    def getGeoDataFromPLZ(self, postCode):
        lat, lng = self.PLZtoGeoCoordConverter.convert(str(postCode))
        if lat == None:
            return

        print(f"PostCode:{postCode} ->  latitude:{lat} longitude:{lng}")


    def createDB(self):
        self.SQLHandler.createNewDB("GasStationData.db")

        self.SQLHandler.createNewTable("GasStationData.db", "gas_station_price_history", [
            "Timestamp TEXT", "Price FLOAT", "ID TEXT", "Name CHAR(20)", "fuelTyp CHAR(20)", "isOpen BIT"])

        self.SQLHandler.createNewTable("GasStationData.db", "gas_station_details", [
             "ID TEXT", "Name CHAR(20)", "Brand TEXT", "Street TEXT", "HouseNr CHAR(8)", "postCode INT", "City TEXT",
             "lat TEXT", "lng Text"]
            )
        self.SQLHandler.createNewTable("GasStationData.db", "best_price_history_last_90_days", ["Timestamp TEXT", "Price FLOAT"])
        self.SQLHandler.createNewTable("GasStationData.db", "statistic", ["statistic", "value"])

        self.SQLHandler.createNewStatistic("best_price_last_period", 100)
        self.SQLHandler.createNewStatistic("best_price_last_period_time_stamp", "")
        self.SQLHandler.createNewStatistic("current_best_price", 100)
        self.SQLHandler.createNewStatistic("current_best_price_time_stamp", "")
        self.SQLHandler.createNewStatistic("last_alert_price", 100)
        self.SQLHandler.createNewStatistic("last_alert_price_time_stamp", "2024-08-31 23:50:23")

        print(f"New Database created in: {ROOT_DB}")



if __name__ == "__main__":

    Setup = Setup()

    # Creates the DB in which the data will be stored
    Setup.createDB()

    # If you don't want to use exact coordinates for the search, you could use the following function
    # to convert a postcode into latitude+longitude
    #postCode = 13347
    #Setup.getGeoDataFromPLZ(postCode)
