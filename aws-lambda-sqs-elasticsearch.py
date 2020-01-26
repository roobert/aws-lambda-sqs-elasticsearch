#!/usr/bin/env python3

import os
import json
from elasticsearch import Elasticsearch


def lambda_handler(event, context):
    es = Elasticsearch(
        [
            {
                "host": os.environ["ELASTICSEARCH_HOST"],
                "port": os.environ["ELASTICSEARCH_PORT"],
                "use_ssl": os.environ["ELASTICSEARCH_SSL"],
            }
        ]
    )

    for record in event["Records"]:
        print("incoming sqs queue message:")
        print(json.dumps(record))

        message = {
            "messageId": record["messageId"],
            "messageAttributes": record["messageAattributes"],
            "body": record["body"],
        }

        print("processed message:")
        print(json.dumps(message))

        response = es.index(index="events", body=json.dumps(message))

        print("elasticsearch response:")
        print(response)
