#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.config import SEARCH_PARAM

class DataTransformer:

    def run(self, gas_station_dict, time_stamp_of_request):

        gas_station_details_dict = self.buildGasStationDetailsDict(gas_station_dict)

        gas_station_list_reduced = self.discardUnnecessaryData(gas_station_dict)
        open_gas_stations = self.discardClosedGasStation(gas_station_list_reduced)
        gas_station_list_sorted = self.sortByPrice(open_gas_stations)
        cheapest_gas_stations = self.cutAfterNCheapestPriceRank(gas_station_list_sorted, n=5)
        cheapest_gas_stations_with_timestamp_of_request = self. addTimestamp(cheapest_gas_stations, time_stamp_of_request)
        cheapest_gas_stations_with_fuelType = self.addFuelType(cheapest_gas_stations_with_timestamp_of_request)

        return cheapest_gas_stations_with_fuelType, gas_station_details_dict



    def buildGasStationDetailsDict(self, gas_station_dict):

        gas_stations = gas_station_dict["stations"]
        gas_station_details_dict = {}

        for gas_station in gas_stations:
            gas_station_details_dict[gas_station["id"]] = {
                "name": gas_station["name"],
                "brand": gas_station["brand"],
                "street": gas_station["street"],
                "houseNumber": gas_station["houseNumber"],
                "postCode": gas_station["postCode"],
                "city": gas_station["place"],
                "lat": gas_station["lat"],
                "lng": gas_station["lng"]
            }

        return gas_station_details_dict




    def discardClosedGasStation(self, gas_station_list_reduced):
        open_gas_stations = []

        for station in gas_station_list_reduced:
            id, price, name, station_is_open = station
            if station_is_open:
                open_gas_stations.append(station)

        return open_gas_stations


    def discardUnnecessaryData(self, gas_station_dict):

        gas_stations = gas_station_dict["stations"]
        gas_station_list_reduced = [[station["id"], station["price"], station["name"], station["isOpen"]] for station in gas_stations]

        return gas_station_list_reduced


    def sortByPrice(self, gas_station_list_reduced):
        return sorted(gas_station_list_reduced, key=lambda x: float(x[1]))


    def cutAfterNCheapestPriceRank(self, gas_stations_price_sorted, n):
        '''Since the gas station list can have a lot of data this function cuts out all stations
           that have a higher ranked price then the given nth rank parameter.
           Example:
               if n = 1 it will only return the gas stations with the current best price.
               if n = 2 it will return also the gas stations that offer the second best price.
        '''

        cheapest_gas_stations = []
        n_cheapest_prices = []
        counter = 0

        for station in gas_stations_price_sorted:
            id, price, name, is_open = station

            if price not in n_cheapest_prices:
                n_cheapest_prices.append(price)
                counter += 1

            if counter == n+1:
                 break

            cheapest_gas_stations.append(station)

        return cheapest_gas_stations


    def addTimestamp(self, cheapest_gas_stations, time_stamp_of_request):
        cheapest_gas_stations_with_timestamp_of_request = [stationdata + [time_stamp_of_request] for stationdata in cheapest_gas_stations]

        return cheapest_gas_stations_with_timestamp_of_request


    def addFuelType(self, cheapest_gas_stations):
        fuelType = SEARCH_PARAM["fuel_type"]
        cheapest_gas_stations_with_fuelType = [stationdata + [fuelType] for stationdata in
                                                           cheapest_gas_stations]

        return cheapest_gas_stations_with_fuelType