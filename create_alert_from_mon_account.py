import boto3
from botocore.exceptions import ClientError


def create_cloudwatch_alarm(distribution_id,metric,sns_arn,ANOMALY_DETECTION_BAND,account_id):
    """
    创建基于 Anomaly Detection 的 CloudWatch 告警
    """
    # 创建 CloudWatch 客户端
    ALARM_NAME = f"CloudFront-{account_id}-{distribution_id}-{metric}-Anomaly"
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

    try:
        # 创建异常检测模型
        response = cloudwatch.put_anomaly_detector(
            MetricName=metric,
            Namespace='AWS/CloudFront',
            Dimensions=[
                {
                    'Name': 'DistributionId',
                    'Value': distribution_id
                },
            ],
            Stat='Sum',

        )
        print(f"==== created detactor model for {ALARM_NAME}==== ")

        # 创建基于异常检测的告警
        response = cloudwatch.put_metric_alarm(
            AlarmName=ALARM_NAME,
            ComparisonOperator='GreaterThanUpperThreshold',
            TreatMissingData = "notBreaching",
            ActionsEnabled = True,
            EvaluationPeriods = 5,
            DatapointsToAlarm = 3,
            Metrics = [
                {
                    "Id": f"m_cdn_{metric}_{account_id}_{distribution_id}",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": "AWS/CloudFront",
                            "MetricName": metric,
                            "Dimensions": [
                                {
                                    "Name": "Region",
                                    "Value": 'Global'
                                },
                                {
                                    "Name": "DistributionId",
                                    "Value": distribution_id
                                }
                            ]
                        },
                        "Period": 60,
                        "Stat": "Sum"
                    },
                    "AccountId": account_id,
                    "ReturnData": True
                },
                {
                    "Id": f"ad_cdn_{metric}_{account_id}_{distribution_id}",
                    "Expression": f"ANOMALY_DETECTION_BAND(m_cdn_{metric}_{account_id}_{distribution_id}, {ANOMALY_DETECTION_BAND})",
                    "Label": f"{metric} (expected)",
                    "ReturnData": True
                }
            ],
            
            ThresholdMetricId=f"ad_cdn_{metric}_{account_id}_{distribution_id}",
            AlarmActions=[sns_arn]
        )

        print(f"已创建告警: {ALARM_NAME}")
    except ClientError as e:
        print(f"创建告警失败: {e}")


