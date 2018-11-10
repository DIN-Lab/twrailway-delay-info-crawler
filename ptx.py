import base64
import hmac
import requests
from datetime import datetime
from hashlib import sha1
from time import mktime
from wsgiref.handlers import format_date_time


class PTX():
    API_BASE_URL = 'https://ptx.transportdata.tw/MOTC/v2'

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_headers(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        params = {
            'username': self.app_id,
            'algorithm': 'hmac-sha1',
            'headers': 'x-date',
            'signature': signature
        }
        joined_params_string = ', '.join(map(lambda ele: '{}="{}"'.format(ele[0], ele[1]), params.items()))

        authorization = 'hmac {}'.format(joined_params_string)

        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

    def get(self, endpoint, params={}):
        url = self.API_BASE_URL + endpoint
        return requests.get(url, params=params, headers=self.get_auth_headers())
