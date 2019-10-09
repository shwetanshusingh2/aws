import boto3
from botocore.client import ClientError
import time
from Week1 import utils as u
import os


os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "C:/Users/Hp/.aws/credentials"

os.environ['AWS_PROFILE'] = "default"
os.environ['AWS_DEFAULT_REGION'] = "ap-south-1"

s3 = boto3.resource('s3')
try:
    s3.create_bucket(Bucket='data-shwet', CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
except ClientError:
    print("Data Bucket Already Created")
u.upload_object('data-shwet', 'template.yaml', 'template.yaml')
u.upload_zip_object('data-shwet', 'lambda_function.py', 'lambda_function.zip', 'lambda_function.zip')
client = boto3.client('cloudformation')
status = u.stack_status('stack')
if status == 'ROLLBACK_COMPLETE' or status == 'ROLLBACK_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE' or status == \
        'DELETE_FAILED':
    u.delete_object('shwet23')
    u.delete_object('shwet23-des')
    client.delete_stack(StackName='stack')
    while u.stack_status('stack') == 'DELETE_IN_PROGRESS':
        time.sleep(1)
    print("stack deleted")
    u.create_stack('stack', 'https://data-shwet.s3.ap-south-1.amazonaws.com/template.yaml', 'shwet23', 'shwet23-des')
    print("stack created")
elif status == 'CREATE_COMPLETE' or status == 'UPDATE_COMPLETE' :
    u.update_stack('stack', 'https://data-shwet.s3.ap-south-1.amazonaws.com/template.yaml', 'shwet23', 'shwet23-des')
    print("stack updated")
else:
    u.create_stack('stack', 'https://data-shwet.s3.ap-south-1.amazonaws.com/template.yaml', 'shwet23', 'shwet23-des')
    print("stack created")