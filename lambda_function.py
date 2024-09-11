import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', ap-south-1')  # Replace 'your-region' with the correct AWS region
    
    # Get list of all stopped instances
    instances = ec2.describe_instances(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['stopped']
    }])
    
    # Extract instance IDs
    instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    
    if instance_ids:
        # Start the instances
        ec2.start_instances(InstanceIds=instance_ids)
        print(f'Starting instances: {instance_ids}')
    else:
        print('No stopped instances found')

    # Return a response after starting instances
    return {
        'statusCode': 200,
        'body': f'Instances started successfully: {instance_ids}' if instance_ids else 'No stopped instances found to start'
    }
