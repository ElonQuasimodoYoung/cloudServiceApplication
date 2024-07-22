# Group 11
# Ziqiang Li, 1173898
# Donghao Yang, 1514687
# Rui Mao, 1469805
# Xiaxuan Du, 1481272
# Ruoyu Lu, 1466195

curl -XPUT -k 'https://127.0.0.1:9200/weatherdata'\
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
            "sort_order": { "type": "integer" },
            "wmo": { "type": "integer" },
            "name": { "type": "text" },
            "history_product": { "type": "keyword" },
            "local_date_time": { "type": "text" },
            "local_date_time_full": { "type": "date", "format": "yyyyMMddHHmmss" },
            "aifstime_utc": { "type": "date", "format": "yyyyMMddHHmmss" },
            "lat": { "type": "float" },
            "lon": { "type": "float" },
            "apparent_t": { "type": "float" },
            "cloud": { "type": "text" },
            "cloud_base_m": { "type": "integer", "null_value": null },
            "cloud_oktas": { "type": "integer", "null_value": null },
            "cloud_type_id": { "type": "integer", "null_value": null },
            "cloud_type": { "type": "text" },
            "delta_t": { "type": "float" },
            "gust_kmh": { "type": "integer" },
            "gust_kt": { "type": "integer" },
            "air_temp": { "type": "float" },
            "dewpt": { "type": "float" },
            "press": { "type": "float" },
            "press_qnh": { "type": "float" },
            "press_msl": { "type": "float" },
            "press_tend": { "type": "text" },
            "rain_trace": { "type": "text" },
            "rel_hum": { "type": "integer" },
            "sea_state": { "type": "text" },
            "swell_dir_worded": { "type": "text" },
            "swell_height": { "type": "float", "null_value": null },
            "swell_period": { "type": "float", "null_value": null },
            "vis_km": { "type": "text" },
            "weather": { "type": "text" },
            "wind_dir": { "type": "text" },
            "wind_spd_kmh": { "type": "integer" },
            "wind_spd_kt": { "type": "integer" }
        }
    }
}'\
   --user 'elastic:elastic' | jq '.'
