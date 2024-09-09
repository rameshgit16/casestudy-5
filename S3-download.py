import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket and file details from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    if not file_key.endswith('.txt'):
        print(f"Skipping non-txt file: {file_key}")
        return

    # Download the file
    tmp_file = '/tmp/' + os.path.basename(file_key)
    s3.download_file(bucket, file_key, tmp_file)
    
    # Count words in the file
    with open(tmp_file, 'r') as file:
        content = file.read()
        word_count = len(content.split())
    
    # Create count.txt with word count and current date
    count_file_key = "count/count.txt"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    count_content = f"File: {file_key}, Word Count: {word_count}, Date: {timestamp}\n"
    
    # Check if count.txt exists, if so download and append to it
    try:
        s3.download_file(bucket, count_file_key, tmp_file)
        with open(tmp_file, 'a') as count_file:
            count_file.write(count_content)
    except s3.exceptions.NoSuchKey:
        # Create new count.txt if it doesn't exist
        with open(tmp_file, 'w') as count_file:
            count_file.write(count_content)
    
    # Upload the updated count.txt to S3
    s3.upload_file(tmp_file, bucket, count_file_key)

    return {
        'statusCode': 200,
        'body': 'Word count processed and updated successfully.'
    }
