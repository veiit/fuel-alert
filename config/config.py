
SEARCH_PARAM = {
    "latitude": "52.52099975265203",
    "longitude": "13.43803882598877",
    "radius_km": "3",
    "sorting": "price",
    "fuel_type": "e5"      # 'e5', 'e10' or 'diesel'
}

BEST_PRICE_PERIOD_LENGTH = 14  # last X days, in which the best price should be found and communicated


# Get the KEY here https://creativecommons.tankerkoenig.de/
API_KEY = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' # replace key

TELEGRAMDATA = {
    "botname": "XXXXXXXX", # Name of the Telegram Bot that is used to send the messages
    "token": "XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", # Replace with a valide TelegramBot Token
    "ID": "000000000" # Replace User ID <- only this Telegram User will get the messages from the TelegramBot
}

ROOT_DATA = "C:\\Folder\\Folder\\FuelAlert\\Data\\"  # Path to the folder where the data should be
ROOT_DB = ROOT_DATA + "SQL_DB\\"
