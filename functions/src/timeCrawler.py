# -*- coding: utf-8 -*-
import logging
import requests
import db
import datetime
import re
from math import floor

logger = logging.getLogger()

def handler(event, context):
  url = 'https://info.sporttery.cn/iframe/lottery_notice.php'
  req = requests.get(url)
  req.encoding='GB2312'
  html = req.text
  
  today = datetime.date.today()
  todayISO = today.isoformat()
  todayCN = '%d月%d日' % (today.month, today.day)
  pattern = '%s竞彩游戏开售时间为(\d{2}:\d{2}),停售时间为(\d{2}:\d{2})' % (todayCN)

  matched = re.findall(re.compile(pattern), html)

  if len(matched) > 0:
    conn = db.getConnection()
    (startTime, stopTime) = matched[0]
    startTimestamp = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (todayISO, startTime), '%Y-%m-%d %H:%M %z')) * 1000)
    stopTimestamp = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (todayISO, stopTime), '%Y-%m-%d %H:%M %z')) * 1000)
    try:
      with conn.cursor() as cursor:
        sql = 'REPLACE INTO `saletime` (`date`, `startTime`, `stopTime`) VALUES (%s, %s, %s)'
        logger.info((todayISO, startTimestamp, stopTimestamp))
        cursor.execute(sql, (todayISO, startTimestamp, stopTimestamp))
      conn.commit()

    finally:
      conn.close()

  return 'Done'