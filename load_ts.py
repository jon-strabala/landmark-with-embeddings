#!/usr/bin/env python3

import os
import json
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import UpsertOptions

# Get Couchbase credentials from environment variables
cb_username = os.getenv("CB_USERNAME")
cb_password = os.getenv("CB_PASSWORD")
cb_hostname = os.getenv("CB_HOSTNAME")

# Connect to the Couchbase cluster
pa = PasswordAuthenticator(cb_username, cb_password)
cluster = Cluster("couchbases://" + cb_hostname + "/?ssl=no_verify", ClusterOptions(pa))

# Open the travel-sample bucket
bucket = cluster.bucket("travel-sample")

# Get the specific collection within the inventory scope
collection = bucket.scope("inventory").collection("landmark")

# Read the JSON file
with open('landmark_all.json') as json_file:
    data = json.load(json_file)

# Insert each document into Couchbase
for document in data:
    key = f"landmark_{document['id']}"
    collection.upsert(key, document)

print("Data loaded successfully!")
