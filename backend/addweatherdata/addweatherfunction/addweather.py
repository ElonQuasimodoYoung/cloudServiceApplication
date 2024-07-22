# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

import logging
import json
import requests
from flask import Flask, current_app
from elasticsearch8 import Elasticsearch

# Define the index name
index_name = "weatherdata"


def main():
    current_app.logger.info(f'Harvested weather data')
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )

    # Fetch data from the API
    data = requests.get('https://reg.bom.gov.au/fwo/IDV60801/IDV60801.94852.json').json()
    current_app.logger.info('Harvested one weather observation')

    # Extract the latest observation
    observations = data.get('observations', {}).get('data', [])
    latest_observations = observations[:1]  # Assuming data is sorted in descending order of time

    for feature in latest_observations:
        res = client.index(
            index=index_name,
            body=feature
        )
    current_app.logger.info('Uploaded latest three weather observations to Elasticsearch')

    return 'OK'
