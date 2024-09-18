#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.config import API_KEY, SEARCH_PARAM
from DataHandler.APIHandler.APICaller import APICaller


class TankerkoenigAPI:

    def __init__(self):
        self.__API_KEY = API_KEY
        self.SEARCH_PARAM = SEARCH_PARAM

        self.APICaller = APICaller()

    def buildListOfGasStationsURL(self):
        '''injects the parameter values from the config file into the search url '''

        url = "https://creativecommons.tankerkoenig.de/json/list.php?"
        url += f"lat={self.SEARCH_PARAM['latitude']}&lng={self.SEARCH_PARAM['longitude']}&"
        url += f"rad={self.SEARCH_PARAM['radius_km']}&sort={self.SEARCH_PARAM['sorting']}&"
        url += f"type={self.SEARCH_PARAM['fuel_type']}&"
        url += "apikey=" + self.__API_KEY

        list_of_gas_stations_url = url

        return list_of_gas_stations_url


    def requestChosenGasStations(self):

        list_of_gas_stations_url = self.buildListOfGasStationsURL()
        call_was_successfull, status, list_of_gas_stations, time_stamp = self.APICaller.makeAPIRequest(list_of_gas_stations_url, "list_of_gas_stations_url")

        return call_was_successfull, status, list_of_gas_stations, time_stamp