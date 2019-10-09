import boto3
import zipfile, os

client = boto3.client('cloudformation')
s3 = boto3.resource('s3')


def create_stack(stack_name, template_url, source, destination):
    response = client.create_stack(
        StackName=stack_name,
        TemplateURL=template_url,
        Capabilities=['CAPABILITY_NAMED_IAM'],
        Parameters = [
        {
            'ParameterKey': "SourceBucket",
            'ParameterValue': source
        },
        {
                'ParameterKey': "DestinationBucket",
                'ParameterValue': destination
        }]
    )


def update_stack(stack_name, template_url, source, destination):
    try:
        response = client.update_stack(
            StackName=stack_name,
            TemplateURL=template_url,
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Parameters=[
                {
                    'ParameterKey': "SourceBucket",
                    'ParameterValue': source
                },
                {
                    'ParameterKey': "DestinationBucket",
                    'ParameterValue': destination
                }]
        )
    except Exception:
        print("No update To Perform")


def stack_status(stack_name):
    try:
        stack = client.describe_stacks(StackName=stack_name)
        status = stack['Stacks'][0]['StackStatus']
        return status
    except Exception:
        return "NO_STACK"


def delete_object(bucket_name):
    try:
        bucket = s3.Bucket(bucket_name)
        bucket.objects.all().delete()
    except Exception:
        print("Bucket Not Present")


def upload_object(bucket_name, filename, location):
    s3.Object(bucket_name, location).upload_file(Filename=filename)


def upload_zip_object(bucket_name, input_filename, output_filename, location):
    zip = zipfile.ZipFile(output_filename, "w")
    zip.write(input_filename, os.path.basename(input_filename))
    zip.close()
    upload_object(bucket_name, output_filename, location)
    os.remove(output_filename)
