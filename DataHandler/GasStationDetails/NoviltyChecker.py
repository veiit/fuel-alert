#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils.Time import getTimestamp
from DataHandler.SQLHandler.SQLHandler import SQLHandler


class NoviltyChecker:

    def __init__(self):
        self.SQLHandler = SQLHandler()


    def checkForNewGasStations(self, gas_station_list):
        known_gas_station_IDs = self.SQLHandler.returnAllKnownGasstationIds()

        new_gas_stations = []

        for gas_station in gas_station_list:
            gas_station_ID = gas_station[0]

            if gas_station_ID not in known_gas_station_IDs:
                new_gas_stations.append(gas_station_ID)

        if len(new_gas_stations) > 0:
            print(f"[{getTimestamp()}][NoviltyChecker] {len(new_gas_stations)} new gas stations were found")

        return new_gas_stations