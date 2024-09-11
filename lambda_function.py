import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    # Get list of all running instances
    instances = ec2.describe_instances(Filters=[{
        'Name': 'instance-state-name', 
        'Values': ['running']
    }])
    
    # Extract instance IDs
    instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    
    if instance_ids:
        # Stop the instances
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f'Stopping instances: {instance_ids}')
    else:
        print('No running instances found')
    
    # Properly formatted return statement
    return {
        'statusCode': 200,
        'body': 'Instances stopped successfully'
    }
