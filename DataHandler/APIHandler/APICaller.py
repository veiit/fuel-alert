#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json
from Utils.Time import getTimestamp


class APICaller:

    def callAPI(self, url):
        '''Makes a Get Request to a given url'''

        headers = {
            "User-agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
        }

        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        status = r.status_code

        return str(status), data


    def makeAPIRequest(self, url, url_name):

        status, data = self.callAPI(url)

        time_stamp = getTimestamp()

        if status == "200":
            return True, status, data, time_stamp

        print('[{}][RequestNewData][ERROR][Status:{}] API - {} kann nicht geladen werden'.format(time_stamp, status, url_name))
        return False, status, data, time_stamp