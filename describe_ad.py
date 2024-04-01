
import boto3
from botocore.exceptions import ClientError

cloudwatch = boto3.client('cloudwatch')
response = cloudwatch.describe_anomaly_detectors(
    Namespace='AWS/CloudFront',
    MetricName='Request',
    Dimensions=[
        {
            'Name': 'DistributionId',
            'Value': 'E3AK4GJ2E4G2CP'
        },
    ],
    AnomalyDetectorTypes=[
        'SINGLE_METRIC','METRIC_MATH'
    ]
)

print(response)
