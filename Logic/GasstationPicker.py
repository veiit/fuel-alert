#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.config import SEARCH_PARAM

from Utils.Time import getTimestamp
from Utils.GeocoordDistanceCalculator import GeocoordDistanceCalculator
from DataHandler.SQLHandler.SQLHandler import SQLHandler

class GasStationPicker:

    def __init__(self):
        self.SEARCH_PARAM = SEARCH_PARAM

        self.SQLHandler = SQLHandler()
        self.GeocoordDistanceCalculator = GeocoordDistanceCalculator()


    def pickWinningGasStation(self, cheapest_gas_stations):

        best_price = self.getBestPrice(cheapest_gas_stations)
        gas_stations_best_price = self.getOnlyGasStationWithBestPrice(best_price, cheapest_gas_stations)
        gas_stations_best_price_with_distances = self.getDistance(gas_stations_best_price)
        gas_stations_best_price_with_distances_sorted = self.sortByDistance(gas_stations_best_price_with_distances)

        winning_gas_station = gas_stations_best_price_with_distances_sorted[0]
        return winning_gas_station, best_price



    def getBestPrice(self, cheapest_gas_stations):
        prices = [i[1] for i in cheapest_gas_stations]
        bestprice = min(prices)
        return bestprice


    def getOnlyGasStationWithBestPrice(self, best_price, cheapest_gas_stations):
        gas_stations_best_price = [i for i in cheapest_gas_stations if i[1] == best_price]
        return gas_stations_best_price


    def getDistance(self, gas_stations_best_price):
        gas_stations_best_price_with_distances = []

        lat = SEARCH_PARAM["latitude"]
        lng = SEARCH_PARAM["longitude"]

        for gas_station in gas_stations_best_price:
            gas_station_id = gas_station[0]

            lat2, lng2 = self.SQLHandler.returnGeoCorFromId(gas_station_id)

            distance = self.GeocoordDistanceCalculator.calculateDistance(lat, lng, lat2, lng2)
            gas_stations_best_price_with_distances.append(gas_station + [distance])

        return gas_stations_best_price_with_distances

    def sortByDistance(self, gas_station_data):
        return sorted(gas_station_data, key=lambda x: float(x[6]))