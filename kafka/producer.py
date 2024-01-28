from kafka import KafkaProducer

# Define the Kafka broker(s) and topic
bootstrap_servers = ['localhost:9092']
topic = 'traffic'

# Create a Kafka producer instance
print("Connecting to Kafka...")
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Produce a message to the specified topic
message_key = b'key'  # You can set a key for the message (optional)
message_value = b'Hello, Kafka!'
producer.send(topic, key=message_key, value=message_value)
print("Message Sent...")

# Flush and close the producer
producer.flush()
producer.close()
