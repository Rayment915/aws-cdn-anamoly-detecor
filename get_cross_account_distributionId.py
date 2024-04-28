# use to list CloudFront distribution ID in source account and create alert in monitoring account

import boto3
from create_alert_from_mon_account import create_cloudwatch_alarm

def get_distribution_list(OwningAccount,next_token = None):
    cloudwatch = boto3.client('cloudwatch')
    metrics = []

    while True:
        # Call the list_metrics API with the appropriate parameters
        if next_token:
            response = cloudwatch.list_metrics(
                Namespace='AWS/CloudFront',
                NextToken=next_token,
                IncludeLinkedAccounts=True,
                OwningAccount=OwningAccount
            )
        else:
            response = cloudwatch.list_metrics(
                Namespace='AWS/CloudFront',
                IncludeLinkedAccounts=True,
                OwningAccount=OwningAccount
            )

        # Append the retrieved metrics to the list
        metrics.extend(response['Metrics'])

        # Check if there are more results to retrieve
        next_token = response.get('NextToken', None)
        if not next_token:
            break

    distribution_ids= [metric['Dimensions'][1]['Value'] for metric in metrics]
    ret=set(distribution_ids)
    return ret

if __name__ == "__main__":
    OwningAccount='YOUR_SOURCE_ACOUNT_ID'
    distributions_list=get_distribution_list(OwningAccount)

    # Modify it according to your use case
    ANOMALY_DETECTION_BAND=5 

    metric_list=['Requests','BytesDownloaded']
    sns_arn='arn:aws:sns:us-east-1:YOUR_MONITORING_ACCOUNT_ID:test-alarm'
    for distribution_id in distributions_list:
        for metric in metric_list:
            create_cloudwatch_alarm(distribution_id,metric,sns_arn,ANOMALY_DETECTION_BAND,OwningAccount)
