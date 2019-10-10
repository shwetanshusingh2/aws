import boto3
from botocore.client import ClientError
import time
import utils as u
import parameters as p
import os



os.environ['AWS_SHARED_CREDENTIALS_FILE'] = p.credential_name

os.environ['AWS_PROFILE'] = p.credential_name
os.environ['AWS_DEFAULT_REGION'] = p.location

s3 = boto3.resource('s3')
try:
    s3.create_bucket(Bucket=p.data_bucket, CreateBucketConfiguration={'LocationConstraint': p.location})
except ClientError:
    print("Data Bucket Already Created")
u.upload_object(p.data_bucket, p.template_name, p.template_name)
u.upload_zip_object(p.data_bucket, 'lambda_function.py', 'lambda_function.zip', 'lambda_function.zip')
client = boto3.client('cloudformation')
status = u.stack_status(p.stack_name)
if status == 'ROLLBACK_COMPLETE' or status == 'ROLLBACK_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE' or status == \
        'DELETE_FAILED':
    u.delete_object(p.names["source_bucket"])
    u.delete_object(p.names["dest_bucket"])
    client.delete_stack(StackName=p.stack_name)
    while u.stack_status('stack') == 'DELETE_IN_PROGRESS':
        time.sleep(1)
    print("stack deleted")
    u.create_stack(p.stack_name, p.names["template_url"], p.names["source_bucket"], p.names["dest_bucket"])
    print("stack created")
elif status == 'CREATE_COMPLETE' or status == 'UPDATE_COMPLETE' :
    u.update_stack(p.stack_name, p.names["template_url"], p.names["source_bucket"], p.names["dest_bucket"])
    print("stack updated")
else:
    u.create_stack(p.stack_name, p.names["template_url"], p.names["source_bucket"], p.names["dest_bucket"])
    print("stack created")
