import json
import boto3
import os
s3 = boto3.resource('s3')
client = boto3.client('s3')
def handler(event, context):
    dest_bucket = s3.Bucket(os.environ['des'])
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3.Object(dest_bucket.name, key).copy_from(CopySource={'Bucket': source_bucket, 'Key': key})