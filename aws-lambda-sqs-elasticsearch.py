#!/usr/bin/env python3

import os
import json
import certifi
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

    print("lambda execution starting")
    for record in event["Records"]:
        print("incoming sqs queue message:")
        print(json.dumps(record))

        print("processed message:")
        message = {
            "messageId": record["messageId"],
            "messageAttributes": record["messageAttributes"],
            "body": record["body"],
        }
        print(json.dumps(message))

        response = es.index(index="events", body=json.dumps(message))

        print("elasticsearch response:")
        print(response)

    print("lambda execution finished")
