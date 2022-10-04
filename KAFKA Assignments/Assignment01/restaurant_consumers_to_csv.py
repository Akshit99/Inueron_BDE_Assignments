import argparse
import pandas as pd
from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient

API_KEY = 'api_key'
ENDPOINT_SCHEMA_URL  = 'https://schema.url'
API_SECRET_KEY = '<---secret--key>'
BOOTSTRAP_SERVER = 'bottstrap.url'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = '<---api--key>'
SCHEMA_REGISTRY_API_SECRET = '<---secret--key>'


def sasl_conf():

    sasl_conf = {'sasl.mechanism': SSL_MACHENISM,
                 # Set to SASL_SSL to enable TLS support.
                #  'security.protocol': 'SASL_PLAINTEXT'}
                'bootstrap.servers':BOOTSTRAP_SERVER,
                'security.protocol': SECURITY_PROTOCOL,
                'sasl.username': API_KEY,
                'sasl.password': API_SECRET_KEY
                }
    return sasl_conf



def schema_config():
    return {'url':ENDPOINT_SCHEMA_URL,
    
    'basic.auth.user.info':f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"

    }


class Order:   
    def __init__(self,record:dict):
        for k,v in record.items():
            setattr(self,k,v)
        
        self.record=record
   
    @staticmethod
    def dict_to_order(data:dict,ctx):
        return Order(record=data)

    def __str__(self):
        return f"{self.record}"


def main(topic):
    
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    
    latest_schema = schema_registry_client.get_latest_version("restaurant-take-away-data-value").schema.schema_str
    
    json_deserializer = JSONDeserializer(latest_schema,
                                         from_dict=Order.dict_to_order)

    consumer_conf = sasl_conf()
    consumer_conf.update({
                     'group.id': 'G2',
                     'auto.offset.reset': "earliest"})

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    
    empty_poll_count = 0 # to check empty message
    msg_records = []
    while empty_poll_count < 20:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                empty_poll_count += 1
                print(f'Poll empty counter: {empty_poll_count}\n\n')
                continue
                
            order = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

            if order is not None:
                empty_poll_count=0
                print("User record {}: order: {}\n"
                      .format(msg.key(), order))
                msg_records.append(order.record)
                
        except KeyboardInterrupt:
            break
    
    consumer.close()
    print(f"Total Messages consumed : {len(msg_records)}")
    print(msg_records)
    df = pd.DataFrame(msg_records)
    return df


df = main("restaurant-take-away-data")

#df.head()
# Store records in csv
df.to_csv('consumed_records.csv')
