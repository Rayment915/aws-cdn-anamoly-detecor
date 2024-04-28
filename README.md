# 背景
AWS 的用户（特别是游戏行业）被DDoS攻击的时候会瞬间产生大量的CloudFront流量，由于缺乏安全意识没有配置CDN告警导致产生大量费用。账单用量告警可能已经是8小时后了，所以我们需要一种及时的CDN 异常的告警方案，而且是能贴合用户实际行为的。

# 方案介绍
AWS CloudWatch 提供原生异常检查的[API](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)，背后帮你生成一个基于过去2周的实际行为生成一个探测的模型，结合CloudFront 我们可以使用Requests 和 BytesDownloaded 两个metric 来自动产生异常的告警。
![Image text](https://github.com/rayment915/aws-cdn-anamoly-detecor/blob/main/img/1.jpg)

### 1. "ANOMALY_DETECTION BAND" 说明
ANOMALY DETECTION BAND 会根据您的指标数据历史趋势,自动计算出一个正常范围,也就是异常检测带。当您的指标数据超出这个正常范围时,CloudWatch 就会将其识别为异常,并向您发送警报。因为每个用户CDN 的用量和使用行为都不一样，所以这个值的设置没有一个固定的最佳实践，可以先从2 开始尝试并在CloudWatch 把预期的图形做出来，值越大指标的正常范围越大。

### 2. 部署步骤
1. 部署前用户需要准备好us-east-1 region的SNS arn 地址用于接收告警
2. 目前只考虑了这两个metric，有需要可以自己增加 metric_list=['Requests','BytesDownloaded']
3. 默认会遍历所有CDN 的distribution_id 都去创建告警
4. 执行部署 python3 CreateMetricsAlarms.py 

# To Partner
如果要在payer 接收告警，可以在linked account 的lambda 接收SNS 通知自行配置告警



