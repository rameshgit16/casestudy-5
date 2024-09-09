import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instances = ['i-instanceID1', 'i-instanceID2']  # Replace with your EC2 instance IDs
    ec2.stop_instances(InstanceIds=instances)
    return 'Stopped instances: ' + str(instances)
  
import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instances = ['i-instanceID1', 'i-instanceID2']  # Replace with your EC2 instance IDs
    ec2.start_instances(InstanceIds=instances)
    return 'Started instances: ' + str(instances)
