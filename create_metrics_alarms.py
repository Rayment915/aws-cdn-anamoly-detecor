import boto3
import os,sys
from create_alert import create_cloudwatch_alarm


# 遍历所有 CloudFront Distribution
def get_list_distributions_list(cloudfront):
    response = cloudfront.list_distributions()
    while True:
        for distribution in response['DistributionList']['Items']:
            print(distribution)
            #print(distribution['Id'])

        # 如果还有更多 Distribution,继续获取
        if 'NextMarker' in response['DistributionList']:
            response = cloudfront.list_distributions(Marker=response['DistributionList']['NextMarker'])
        else:
            break

if __name__ == "__main__":
    cloudfront = boto3.client('cloudfront') 
    get_list_distributions_list(cloudfront)
    ANOMALY_DETECTION_BAND=5
    metric_list=['Requests','BytesDownloaded']
    sns_arn='arn:aws:sns:us-east-1:xxxxx:test-alarm'
    distribution_id='xxxx'
    for metric in metric_list:
        create_cloudwatch_alarm(distribution_id,metric,sns_arn,ANOMALY_DETECTION_BAND)


    

