import boto3
import os
import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
   
    # Check if the file is in the /out folder
    if file_key.startswith('out/') and file_key.endswith('.txt'):
        # Download the file from S3
        temp_file = '/tmp/' + os.path.basename(file_key)
        s3.download_file(bucket_name, file_key, temp_file)
       
        # Read the file and count words
        with open(temp_file, 'r') as file:
            file_content = file.read()
            word_count = len(file_content.split())
       
        # Prepare the output for count.txt file
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = os.path.basename(file_key)  # Extract the file name
        output = f"File: {file_name}, Word Count: {word_count}, Executed at: {current_time}\n"
       
        # Append to count.txt (or create if it doesn't exist)
        count_file_key = 'count/count.txt'
        temp_count_file = '/tmp/count.txt'
       
        # Download the existing count.txt if available, otherwise create a new one
        try:
            s3.download_file(bucket_name, count_file_key, temp_count_file)
        except Exception as e:
            with open(temp_count_file, 'w') as count_file:
                count_file.write('')
       
        # Append the new word count and file name
        with open(temp_count_file, 'a') as count_file:
            count_file.write(output)
       
        # Upload the updated count.txt back to S3
        s3.upload_file(temp_count_file, bucket_name, count_file_key)
       
        return {
            'statusCode': 200,
            'body': f'Word count for {file_key} appended to /count/count.txt'
        }

    else:
        return {
            'statusCode': 400,
            'body': 'Invalid file or location'
        }
