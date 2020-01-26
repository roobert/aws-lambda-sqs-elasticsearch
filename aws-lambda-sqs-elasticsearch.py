#!/usr/bin/env python3

import json
import argparse
from elasticsearch import Elasticsearch


def lambda_handler(event, context):
    args = parse_args()
    es = Elasticsearch(
        [
            {
                "host": args.elasticsearch_host,
                "port": args.elasticsearch_port,
                "use_ssl": args.elasticsearch_ssl,
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="SQS queue triggered lambda which writes messages to Elasticsearch domain"
    )

    parser.add_argument(
        "--elasticsearch-host", help="elasticsearch host", required=True
    )
    parser.add_argument(
        "--elasticsearch-port", help="elasticsearch port", required=True
    )
    parser.add_argument(
        "--elasticsearch-ssl", help="enable ssl for elasticsearch connection", type=bool
    )

    return parser.parse_args()
