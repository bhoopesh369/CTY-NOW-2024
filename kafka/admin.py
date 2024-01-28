from kafka import KafkaAdminClient

# Set your Kafka bootstrap servers
bootstrap_servers = 'your_kafka_bootstrap_servers'

# Create an admin client
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

# Get the list of topics
topics = admin_client.list_topics()

# Print the list of topics
print("List of topics:", topics)

# Close the admin client
admin_client.close()