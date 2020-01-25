#!/usr/bin/env python3

import json
import boto3
import argparse
from elasticsearch import Elasticsearch


def main():
    args = parse_args()
    sqs = boto3.resource("sqs")
    es = Elasticsearch(
        [
            {
                "host": args.elasticsearch_host,
                "port": args.elasticsearch_port,
                "use_ssl": args.elasticsearch_ssl,
            }
        ]
    )

    queue = sqs.get_queue_by_name(QueueName=args.sqs_queue_name)

    while True:
        for sqs_message in queue.receive_messages():
            es_message = {"MessageId": sqs_message.message_id, "Body": sqs_message.body}
            print(json.dumps(es_message))
            response = es.index(index="events", body=json.dumps(es_message))
            print(response["result"])
            sqs_message.delete()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read messages from an SQS queue and write them to an Elasticsearch domain"
    )

    parser.add_argument("--sqs-queue-name", help="sqs queue name", required=True)
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


if __name__ == "__main__":
    main()
