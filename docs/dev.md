# 开发说明

## 部署方式
1. 安装 VSCode 的 Aliyun Serverless 插件。安装文档：https://help.aliyun.com/document_detail/126086.html
2. 复制 `template.example.yml` 为 `template.yml`，将其中所有纯大写字母的变量替换为实际值

## 文件说明：
```
├── create_table.sql // 数据库建表语句
├── functions  // 函数计算源码
│   ├── src  // python 函数的源码
│   └── trendImageSaver  // 走势图保存函数的源码，nodejs
├── template.example.yml  // 函数计算配置文件模板
└── trends_web  // 趋势图页面
```

## 函数说明：
 * crawler:  sporttery.cn 官方数据抓取函数
 * apiMatchGetFootball:  /match/getFootball API 实现
 * timeCrawler:  sporttery.cn 赛事安排中的开售时间、停售时间抓取
 * resultCrawler:  sporttery.cn 赛果抓取
 * matchDetailCrawler:  sporttery.cn 赛事详细信息抓取
 * trendImage:  30天走势图生成 API，输出一个网页
 * trendImageSaver:  30天走势图保存函数，用 chrome headless 将 trendImage 输出的网页转为图片并保存到七牛
 * matchStatusCrawler:  sporttery.cn 赛事状态抓取
 * apiResultCalcBonus:  /result/calcBonus API实现
 * apiResultPredictTime:  /result/predictTime API 实现
 * f500MatchInfoCrawler:  500.com 赛事基础数据抓取
