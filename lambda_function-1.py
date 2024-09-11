import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    # Example logic: List running EC2 instances
    instances = ec2.describe_instances(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']
    }])
    
    instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]
    
    if instance_ids:
        ec2.stop_instances(InstanceIds=instance_ids)
        print(f'Stopping instances: {instance_ids}')
    else:
        print('No running instances found')

    # Ensure the return statement is properly formatted and closed
    return {
        'statusCode': 200,
        'body': 'Instances stopped successfully'
    }
