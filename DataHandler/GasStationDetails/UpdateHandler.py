#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.Time import getTimestamp

from DataHandler.SQLHandler.SQLHandler import SQLHandler

from DataHandler.GasStationDetails.NoviltyChecker import NoviltyChecker


class UpdateHandler:
    def __init__(self):

        self.SQLDB = SQLHandler()
        self.NoviltyChecker = NoviltyChecker()


    def run(self, cheapest_gas_stations, gas_station_details_dict):
        new_gas_stations = self.NoviltyChecker.checkForNewGasStations(cheapest_gas_stations)

        for gas_station in new_gas_stations:
            if gas_station not in gas_station_details_dict:
                print(f"[{getTimestamp()}][UpdateHandler] No GasStation Details can be retrieved from Price API for ID: {gas_station}")
                continue

            self.saveGasStationDetailsInDB(gas_station_details_dict[gas_station], gas_station)



    def saveGasStationDetailsInDB(self, gas_station_details, gas_station_id):

        was_successfull = self.SQLDB.addNewGasStationDetails(
                                           gas_station_id,
                                           name=gas_station_details["name"],
                                           brand=gas_station_details["brand"],
                                           street= gas_station_details["street"],
                                           houseNr=gas_station_details["houseNumber"],
                                           postCode=gas_station_details["postCode"],
                                           city=gas_station_details["city"],
                                           lat=gas_station_details["lat"],
                                           lng=gas_station_details["lng"]
                                    )

        return was_successfull