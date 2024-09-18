import time
from datetime import datetime, date


def getTimestamp():
    date_time = datetime.fromtimestamp(time.time())
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


def isTimestampOlderThenXdays(time_stamp, days):
    datetime_obj = datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    time_stamp_unix = datetime_obj.timestamp()

    now_unix = time.time()
    offset = days * 60 * 60 * 24

    if time_stamp_unix < now_unix - offset:
        return True

    return False



