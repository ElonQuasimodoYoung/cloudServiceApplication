# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

import logging, json, requests, socket
from flask import current_app
from elasticsearch8 import Elasticsearch

def main():

    current_app.logger.info(f'Harvested one weather observation')
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    url = "https://data.ballarat.vic.gov.au/api/explore/v2.1/catalog/datasets/air-quality-observations/records?order_by=date_time%20DESC&limit=100"

    response = requests.get(url)
    data = response.json().get('results',[])
    last_observation = data[:1]
    for feature in last_observation:
        res = client.index(
            index='air',
            body=feature,
        )
        current_app.logger.info(f'Added {feature}')
    return 'OK'
