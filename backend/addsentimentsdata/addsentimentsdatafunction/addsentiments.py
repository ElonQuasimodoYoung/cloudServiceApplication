# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

import logging, json, requests
from flask import current_app, request
from requests.auth import HTTPBasicAuth
from elasticsearch8 import Elasticsearch


def pull(startDate, endDate):
    current_app.logger.info(f'Received request: ${request.headers}')

    API_KEY = "de390ab4bbd79a00d49bd69a810e33a7"
    url = "https://api.ado.eresearch.unimelb.edu.au/login"
    res = requests.post(url, auth=HTTPBasicAuth('apikey', API_KEY))
    if res.ok:
        jwt = res.text
    data_url = 'https://api.ado.eresearch.unimelb.edu.au/analysis/place/collections/twitter'
    qs_params = {
        'startDate': startDate,
        'endDate': endDate,
        'aggregationLevel': 'gccsa',
        'sentiment': True
    }
    headers = {'Authorization': f"Bearer {jwt}"}
    res = requests.get(data_url, headers=headers, params=qs_params)
    data = res.json()
    if not data:
        current_app.logger.info(f'No data provided from {startDate} to {endDate}')
        return 'Error'

    current_app.logger.info(f'Harvested sentiments')
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )
    for feature in data:
        res = client.index(
            index='sentiments_{}'.format(startDate),
            body=feature
        )
        current_app.logger.info(f'Data added: from: {startDate} to {endDate}')

    return 'OK'


def main():
    for i in range(1, 13):
        startDate = '2021-0{}-02'.format(i)
        endDate = '2021-0{}-01'.format(i + 1)

        if i > 9:
            startDate = '2021-{}-02'.format(i)
            endDate = '2021-{}-01'.format(i + 1)
        if i == 9:
            endDate = '2021-{}-01'.format(10)
        if i == 1:
            startDate = '2021-01-01'
        if i == 12:
            endDate = '2021-12-31'
        print(f'Starting {startDate} to {endDate}')
        pull(startDate, endDate)
