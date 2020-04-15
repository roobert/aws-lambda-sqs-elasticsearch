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
        body = json.loads(record["body"])
        message = {
            "messageId": record["messageId"],
            "messageAttributes": record["messageAttributes"],
            "payload": body,
        }

        print(json.dumps(message))

        response = es.index(
            index="events", doc_type="generated", body=json.dumps(message)
        )

        print("elasticsearch response:")
        print(response)

    print("lambda execution finished")
