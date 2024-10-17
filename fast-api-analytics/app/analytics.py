from kafka import KafkaProducer, KafkaConsumer
from elasticsearch import Elasticsearch
import json
import os


# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[os.getenv("KAFKA_BOOTSTRAP_SERVERS")],
    # bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'url_access_events',  # Replace with your topic name
    bootstrap_servers='kafka:9092',  # Your Kafka broker address
    auto_offset_reset='earliest',  # Start reading at the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

# for message in consumer:
#     print(f"Received message: {message.value}")

# # Initialize Elasticsearch client
# es = Elasticsearch([os.getenv("ELASTICSEARCH_URL")])

# async def send_event_click_event(click_data: dict):
def send_event_click_event(click_data: dict):
    """Asynchronously send click event to Kafka."""
    """Send analytics event to Kafka."""
    # event = {
    #     "url": url,
    #     "referrer": referrer,
    #     "location": location,
    # }
    
    producer.send('url_access_events', click_data)
    
    print("data sent")

# def store_event_in_elasticsearch(event):
#     """Store the analytics event in Elasticsearch."""
#     es.index(index='url_analytics', document=event)

# def get_top_referrers():
#     """Retrieve top referrers from Elasticsearch."""
#     response = es.search(
#         index='url_analytics',
#         body={
#             "size": 10,
#             "aggs": {
#                 "top_referrers": {
#                     "terms": {
#                         "field": "referrer.keyword",
#                         "size": 10
#                     }
#                 }
#             }
#         }
#     )
#     return response['aggregations']['top_referrers']['buckets']

# def get_active_locations():
#     """Retrieve most active locations from Elasticsearch."""
#     response = es.search(
#         index='url_analytics',
#         body={
#             "size": 10,
#             "aggs": {
#                 "active_locations": {
#                     "terms": {
#                         "field": "location.keyword",
#                         "size": 10
#                     }
#                 }
#             }
#         }
#     )
#     return response['aggregations']['active_locations']['buckets']
