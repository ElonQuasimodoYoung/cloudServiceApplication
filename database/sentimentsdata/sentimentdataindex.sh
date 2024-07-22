# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

curl -XPUT -k 'https://127.0.0.1:9200/sentiments'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "dynamic":"true",
        "properties": {
            "sentiment": {
                "type": "float"
            }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'