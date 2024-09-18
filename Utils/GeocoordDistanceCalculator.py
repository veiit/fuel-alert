#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geopy import distance


class GeocoordDistanceCalculator:

    def calculateDistance(self, lat, lng, lat2, lng2):
        return distance.distance((lat,lng), (lat2, lng2)).km

