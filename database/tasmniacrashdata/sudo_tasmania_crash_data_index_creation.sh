# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

curl -XPUT -k 'https://127.0.0.1:9200/crashdata'\
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
            "light_condition": {
                "type": "text"
            },
            "crash_date": {
                "type": "date"
            },
            "severity": {
                "type": "text"
            },
            "location_description": {
                "type": "text"
            },
            "centre_line": {
                "type": "text"
            },
            "visited": {
                "type": "text"
            },
            "id": {
                "type": "integer"
            },
            "report_date": {
                "type": "date"
            },
            "description": {
                "type": "text"
            },
            "vcrn": {
                "type": "text"
            },
            "longitude": {
                "type": "double"
            },
            "latitude": {
                "type": "double"
            },
            "surface_type": {
                "type": "text"
            },
            "speed_zone": {
                "type": "text"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
