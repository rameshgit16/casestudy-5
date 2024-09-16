import boto3
import os
import datetime
import logging
import json
import botocore.exceptions

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def lambda_handler(event, context):
    # Log the entire event to verify the structure and values
    logger.info(f"Event Data: {json.dumps(event)}")
    
    # Get bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Log bucket name and file key for debugging
    logger.info(f"Bucket Name: {bucket_name}")
    logger.info(f"File Key: {file_key}")

    # Check if the file is in the /out folder and is a text file
    if file_key.startswith('out/') and file_key.endswith('.txt'):
        # Attempt to download the file from S3
        try:
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            file_content = response['Body'].read().decode('utf-8')
            logger.info(f"File Content (first 100 chars): {file_content[:100]}")  
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                logger.error(f"File not found: {file_key}")
                return {'statusCode': 404, 'body': json.dumps({'error': 'File not found'})}
            else:
                logger.error(f"Error downloading file: {e}")
                return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

        # Count words
        word_count = len(file_content.split())

        # Prepare the output for count.txt file
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = os.path.basename(file_key)
        output = f"File: {file_name}, Word Count: {word_count}, Executed at: {current_time}\n"

        # Append to count.txt (or create if it doesn't exist)
        count_file_key = 'count/count.txt'

        try:
            response = s3.get_object(Bucket=bucket_name, Key=count_file_key)
            existing_content = response['Body'].read().decode('utf-8')
            updated_content = existing_content + output
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                updated_content = output
            else:
                logger.error(f"Error downloading count.txt: {e}")
                return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

        # Upload the updated count.txt back to S3
        try:
            s3.put_object(Bucket=bucket_name, Key=count_file_key, Body=updated_content)
        except botocore.exceptions.ClientError as e:
            logger.error(f"Error uploading count.txt: {e}")
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    return {'statusCode': 200, 'body': 'Processing complete'}
