#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.config import ROOT_DATA

class PLZtoGeoCoordConverter:

    def __init__(self):
        self.PLZGeocoordDict = self.loadData()


    def loadData(self):
        PLZGeocoordDict = {}

        with open (ROOT_DATA + "plz_geocoord.csv", "r") as csvfile:
            data = csvfile.readlines()

        for row in data:
             plz, lat, lng = row.split(",")
             lng = lng.split("\n")[0]

             PLZGeocoordDict[plz] = {
                 "lat": lat,
                 "lng": lng
             }

        return PLZGeocoordDict


    def convert(self, plz):

        plz = str(plz)

        if len(plz) != 5:
            print(f'[ERROR] The post code:"{plz}" is wrong. The code should be exact 5 digits!')
            return None, None

        if plz not in self.PLZGeocoordDict:
            print(f"[ERROR] For the following post code:{plz} is no data available. Please check the post code again!")
            return None, None

        return self.PLZGeocoordDict[plz]["lat"], self.PLZGeocoordDict[plz]["lng"]