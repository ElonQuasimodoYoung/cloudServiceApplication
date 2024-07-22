# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

curl -XPUT -k 'https://127.0.0.1:9200/air'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "device_id": {
                "type": "text"
            },
            "date_time": {
              "type": "date"
            },
            "location_description": {
              "type": "text"
            },
            "latitude": {
              "type": "float"
            },
            "longitude": {
              "type": "float"
            },
            "pm1": {
              "type": "integer"
            },
            "pm25": {
              "type": "integer"
            },
            "pm10": {
              "type": "integer"
            },
            "ozone": {
              "type": "integer"
            },
            "nitrogen_dioxide": {
              "type": "integer"
            },
            "carbon_monoxide": {
              "type": "integer"
            },
            "air_quality_category": {
              "type": "text"
            },
            "point": {
              "type": "geo_point"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
