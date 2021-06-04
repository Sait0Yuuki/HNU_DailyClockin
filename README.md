# HNU_DailyClockin

## Usage

1. fork仓库

2. 在fork的仓库内的Settings->Secrets中添加如下条目

| secrets          | 说明           | 备注                                                   |
| ---------------- | -------------- | ------------------------------------------------------ |
| SECRET_ID    | TX OCR API    |     https://console.cloud.tencent.com/cam/capi                                                 |
| SECRET_KEY | TX OCR SECRET |                                                        |
| ID         | 打卡账号       |                                                        |
| PASSWORD   | 打卡密码       |                                                        |
| BARK |   |  |

3. 打开仓库的action
+ action触发机制
	+ push后自动触发 
	+ 在action中点击Run workflow
	+ 每日自动在00:15执行
		+ 时间修改：`.github/workflows/clockin.yml`中

```
  schedule:
 - cron: '15 16 * * *' #UTC时间，参考https://crontab.guru/
```
