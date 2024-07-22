# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

import json
import unittest
import requests
import json


def getdata(index, data):
    url = f"https://127.0.0.1:9200/{index}/_search"
    headers = {
        "Content-Type": "application/json"
    }
    auth = ("elastic", "elastic")
    response = requests.get(url, headers=headers, json=data, auth=auth, verify=False)
    result = response.json()
    return result['hits']['total']['value']


class TestGetData(unittest.TestCase):
    def test_getincome(self):
        index = 'income*'
        # size: the max size limit of data returned
        data = {
            "size": 1000,
        }

        json_response = getdata(index, data)
        self.assertEqual(json_response, 16)

    def test_getsentiment(self):
        index = 'sentiment*'
        data = {
            "size": 2000,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "country": "au"
                            }
                        }
                    ]
                }
            }
        }
        json_response = getdata(index, data)
        self.assertEqual(json_response, 822)

    def test_getweather(self):
        index = 'weather*'
        # size: the max size limit of data returned
        data = {
            "size": 1000,
        }
        json_response = getdata(index, data)
        # attention: the count of weather data is dynamic
        self.assertEqual(json_response, 262)

    def test_getair(self):
        index = 'air*'
        # size: the max size limit of data returned
        data = {
            "size": 1000,
        }

        json_response = getdata(index, data)
        # attention: the count of air data is dynamic
        self.assertEqual(json_response, 316)

    def test_getcrash(self):
        index = 'crash*'
        # size: the max size limit of data returned
        data = {
            "size": 10000,
        }

        json_response = getdata(index, data)
        self.assertEqual(json_response, 10000)


if __name__ == '__main__':
    unittest.main()
