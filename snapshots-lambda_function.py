
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    # Find snapshots older than 14 days
    old_snapshots = []
    cutoff = datetime.now() - timedelta(days=14)
    
    for snapshot in snapshots:
        snapshot_time = snapshot['StartTime'].replace(tzinfo=None)
        if snapshot_time < cutoff:
            old_snapshots.append(snapshot['SnapshotId'])
    
    # Delete old snapshots
    for snapshot_id in old_snapshots:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Deleted snapshot: {snapshot_id}")
    
    return {
        'statusCode': 200,
        'body': f"Deleted {len(old_snapshots)} snapshots."
    }
