#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from config.config import ROOT_DB


class SQLHandler:

    # INSERT/UPDATE Data in DB

    def addNewStationPrices(self, gas_station_price_list):
        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                for gas_station in gas_station_price_list:
                    gas_station_id, price, name, is_open, timestamp_of_price_request, fuel_type = gas_station
                    sql = '''INSERT INTO gas_station_price_history(Timestamp,Price,ID,Name, fuelTyp, isOpen) VALUES(?,?,?,?,?,?) '''
                    cur = conn.cursor()
                    cur.execute(sql, (timestamp_of_price_request, price, gas_station_id, name, fuel_type, is_open))
                    #print(timestamp_of_price_request, price, gas_station_id, name, fuel_type, is_open)
                    conn.commit()

            return True


        except sqlite3.Error as e:
            print(e)
            return False


    def addNewBestPrice(self, best_price, timestamp_of_price_request):

        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = '''INSERT INTO best_price_history_last_90_days(Timestamp,Price) VALUES(?,?) '''
                cur = conn.cursor()
                cur.execute(sql, (timestamp_of_price_request, best_price))
                conn.commit()

            return True

        except sqlite3.Error as e:
            print(e)
            return False


    def addNewGasStationDetails(self, gas_station_id, name, brand, street, houseNr, postCode, city, lat, lng):

        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = '''INSERT INTO gas_station_details(ID, Name, Brand, Street, HouseNr, postCode, City, lat, lng) VALUES(?,?,?,?,?,?,?,?,?) '''
                cur = conn.cursor()
                cur.execute(sql, (gas_station_id, name, brand, street, houseNr, postCode, city, lat, lng))
                conn.commit()

            return True

        except sqlite3.Error as e:
            print(e)
            return False


    def updateStatisticValue(self, statistic, value):
        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = '''UPDATE statistic SET value = ?  WHERE statistic = ?'''
                cur = conn.cursor()
                cur.execute(sql, (value, statistic))
                conn.commit()

            return True

        except sqlite3.Error as e:
            print(e)
            return False

    # RETURN VALUES

    def returnStatisticValue(self, valueName):
        data = None
        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = f'''SELECT value
        FROM statistic
        WHERE statistic = '{valueName}';'''
                cur = conn.cursor()
                cur.execute(sql)
                data = cur.fetchall()
                conn.commit()

            return data[0][0]

        except sqlite3.Error as e:
            print(e)
            return None


    def returnBestPricesInLastXDays(self, x):
        data = []
        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = f'''SELECT Timestamp, Price
                    FROM best_price_history_last_90_days
                    WHERE Timestamp >= datetime('now', '-{x} days')
                    ORDER BY Timestamp;'''
                cur = conn.cursor()
                cur.execute(sql)
                data = cur.fetchall()
                conn.commit()

        except sqlite3.Error as e:
            print(e)

        return data



    def returnAllKnownGasstationIds(self):
        data = []
        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = f'''SELECT ID
        FROM gas_station_details;'''
                cur = conn.cursor()
                cur.execute(sql)
                data = cur.fetchall()
                conn.commit()

            data = [i[0] for i in data]

            return data

        except sqlite3.Error as e:
            print(e)
            return []

    def returnGeoCorFromId(self, gas_station_id):

        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = f'''SELECT lat, lng FROM gas_station_details WHERE ID = "{gas_station_id}";'''
                cur = conn.cursor()
                cur.execute(sql)
                data = cur.fetchall()
                conn.commit()

            lat, lng = data[0]
            return lat, lng

        except sqlite3.Error as e:
            print(e)
            return 0, 0


    def returnGasStationDetailsFromId(self, gas_station_id):

        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = f'''SELECT Name, Brand, Street, HouseNr, postCode, City  FROM gas_station_details WHERE ID = "{gas_station_id}";'''
                cur = conn.cursor()
                cur.execute(sql)
                data = cur.fetchall()
                conn.commit()

            name, brand, street, houseNr, postCode, city = data[0]
            return name, brand, street, houseNr, postCode, city

        except sqlite3.Error as e:
            print(e)
            return 0, 0







    # Helper functions for setup and testing
    def createNewDB(self, filename):
        conn = None
        try:
            conn = sqlite3.connect(ROOT_DB + filename)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


    def createNewTable(self, filename, tabel_name, Col):

        with sqlite3.connect(ROOT_DB + filename) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {tabel_name}")

            # Creating table as per requirement
            sql = f'CREATE TABLE {tabel_name}(\n {Col[0]}'
            for name_and_type in Col[1:]:
                sql += f",\n {name_and_type}"
            sql += '\n)'

            print(sql)

            cursor.execute(sql)
            print(f"{tabel_name} created successfully")

            conn.commit()


    def createNewStatistic(self, statistic_name, value):

        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = '''INSERT INTO statistic(statistic,value) VALUES(?,?) '''
                cur = conn.cursor()
                cur.execute(sql, (statistic_name, value))
                print(statistic_name, value)
                conn.commit()

            return True

        except sqlite3.Error as e:
            print(e)
            return False

    def deleteTable(self, table_name):

        try:
            with sqlite3.connect(ROOT_DB + 'GasStationData.db') as conn:
                sql = f'''DROP TABLE {table_name}'''
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
            return True

        except sqlite3.Error as e:
            print(e)
            return False