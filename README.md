# FuelAlert

This service monitors fuel prices in a specified area and sends an alert (currently only via a Telegram bot) when the price reaches a new low.

The alert message includes the price, details of the gas station, and the distance to the station.

<br>
<br>

## How to Set Up the Service
### 1) Obtain API Tokens
#### 1.1 API Key for Fuel Prices from the Tankerkoenig API

This service uses data provided by the Tankerkoenig API. <br>
You can get an API key here: [Tankerkoenig API](https://creativecommons.tankerkoenig.de).

#### 1.2 Telegram Bot

This service uses a Telegram bot to send messages.<br>
Other communication methods could be implemented by modifying the method Communication.Messenger.sendMsg().<br>
In version 1.0, no other alert methods are implemented.<br>

To configure Telegram messages, you need to create a new Telegram bot and obtain its token.<br>
More information: [Creating a new bot](https://core.telegram.org/bots/features#creating-a-new-bot).

### 2) Configure the Settings File
The service uses settings stored in the config.config Python file. <br>
You need to provide the following information:

#### 2.1 SEARCH_PARAM

This dictionary specifies the area and fuel type for price searches: <br>

* __latitude + longitude__: Set the location where you want to search for fuel prices.
    You can use the method Setup.getGeoDataFromPLZ(plz) to convert your postal code (PLZ) into latitude and longitude.
* __radius_km__: Define how far from the location you want to search for fuel prices.
* __fuel_type__: Specify the type of fuel you want prices for. You can choose between 'e5', 'e10', or 'diesel'.

#### 2.2 BEST_PRICE_PERIOD_LENGTH

The service uses a rolling window to track the minimum prices. <br>
Provide a value in days for the period during which the best price should be found and notified.

For example, a value of 14 means the service will alert you if the current price drops below the minimum price in the last 14 days.
#### 2.3 API Keys

* __API_KEY__: API key from Tankerkoenig.
* __TELEGRAMDATA.token__: Token from the newly created Telegram bot.
* __TELEGRAMDATA.id__: Your ID, so that only you receive the Telegram messages.

#### 2.4 ROOT_DATA

Specify the path where the data should be saved.
### 3) Create a New Database

If you have provided a valid path for ROOT_DATA in config.config, you can set up the database by calling Setup.createDB().
