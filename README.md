# AWS Lambda SQS Elasticsearch

## About
Read messages from an SQS queue and write them to an Elasticsearch domain.

## Example

```
export AWS_DEFAULT_REGION="<region>"
./aws-lambda-sqs-elasticsearch.py \
  --sqs-queue-name <queue name> \
  --elasticsearch-host <address> \
  --elasticsearch-port 443 \
  --elasticsearch-ssl true
```
