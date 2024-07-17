## landmark-with-embeddings

This data set is designed to replace the keyspace `travel-sample`.`inventory`.`landmark` with the data in the file "*landmark_all.json*".
It contains the same data as the collection `landmark` but we get an embedding based on the value `name  + " " +  content`

* embedding_crc
+ A CRC `name  + " " +  content` (note, the CRC includes the double quotes)

* embedding
+ This is an OpenAI text-embedding-ada-002 embedding with dimension 1536

The data file "*landmark_all.json*" is 147,348,261 bytes, with most of the size due to the JSON array vectors in for the field `embedding`

## Prerequisites 

You will need a Couchbase database with the sample dataset travel-smaple pre-loaded 

Your Couchbase version should be 7.6.0 or greater (newer versions like 7.6.2 will run faster).

## How to Load (from an OnPrem server) into an OnPrem server or Capella

```bash
cbimport json -c couchbases://${CB_HOSTNAME} \
    -no-ssl-verify \
    -u $CB_USERNAME -p $CB_PASSWORD \
    -b travel-sample \
    -f list -d file://./landmark_all.json \
    --scope-collection-exp inventory.landmark \
    -g landmark_%id%
```

## How to Load via Python into an OnPrem server or Capella

Install the SDK via

 * pip install couchbase

Confiugre your environment variables

* CB_USERNAME
* CB_PASSWORD
* CB_HOSTNAME

Run the follwoing program 

* python3 load_ts.py

```python3
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
```



## The result will be two new fields in your JSON documents 
```json
  "embedding_crc": "60530323380d1d69",
  "embedding": [-0.010101266205310822, 0.002630329690873623, <<1534 items removed>> ],
```
