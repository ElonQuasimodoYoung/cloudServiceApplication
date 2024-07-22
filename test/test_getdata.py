# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

import json

import requests
import unittest


def getdatafromurl(part_of_url):
    url = f"http://127.0.0.1:9090/{part_of_url}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return "Error:", response.status_code


class TestGetDataFunction(unittest.TestCase):
    def test_getsentiment_sum(self):
        part_of_url = "sentiments/country/au/field/sentiment"
        result = getdatafromurl(part_of_url)
        result = result['sum_sentiment']['value']
        self.assertEqual(result, 34041.92032577284, "get sum of sentiment in Aus correctly")

    def test_getsentiment_count_sum(self):
        part_of_url = "sentiments/country/au/field/sentimentcount"
        result = getdatafromurl(part_of_url)
        result = result['sum_sentiment']['value']
        self.assertEqual(result, 325354.0, "get sum of sentimentcount in Aus correctly")

    def test_getcrashbyspeed_all(self):
        part_of_url = "crash/field/speed_zone/para/all"
        result = getdatafromurl(part_of_url)
        groundtruth = {'040': '1752.0', '050': '23847.0', '060': '10080.0', '070': '2704.0', '080': '6831.0',
                       '090': '524.0', '100': '9807.0', '110': '2140.0', '<40': '8122.0', 'Not Known': '4748.0'}

        self.assertEqual(result, groundtruth, "get count of crashes of each speed correctly")

    def test_getcrashbyspeed_lessthan40(self):
        part_of_url = "crash/field/speed_zone/para/<40"
        result = getdatafromurl(part_of_url)
        groundtruth = 8122.0
        self.assertEqual(result, groundtruth, "get count of crashed of speed less than 40 correctly")

    def test_getcrashbylightcondition_all(self):
        part_of_url = "crash/field/light_condition/para/all"
        result = getdatafromurl(part_of_url)
        groundtruth = {'Darkness (with street light)': '13087.0',
                       'Darkness (without street light)': '13087.0',
                       'Dawn / Dusk': '3522.0',
                       'Daylight': '53155.0',
                       'Not known': '788.0'}
        self.assertEqual(result, groundtruth, "get count of crashed of each light condition correctly")

    def test_getcrashbylightcondition_daylight(self):
        part_of_url = "crash/field/light_condition/para/Daylight"
        result = getdatafromurl(part_of_url)
        groundtruth = 53155.0
        self.assertEqual(result, groundtruth, "get count of crashed of daylight correctly")

    def test_getcrashbyseverity_all(self):
        part_of_url = "crash/field/severity/para/all"
        result = getdatafromurl(part_of_url)
        groundtruth = {'Fatal': '328.0', 'First Aid': '4872.0', 'Minor': '11568.0', 'Property Damage Only': '48764.0',
                       'Serious': '2513.0'}
        self.assertEqual(result, groundtruth, "get count of crashed of each severity correctly")

    def test_getcrashbyseverity_fatal(self):
        part_of_url = "crash/field/severity/para/Fatal"
        result = getdatafromurl(part_of_url)
        groundtruth = 328.0
        self.assertEqual(result, groundtruth, "get count of crashed of fatal correctly")


if __name__ == '__main__':
    unittest.main()
