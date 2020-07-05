# -*- coding: utf-8 -*-
import logging
import json
import requests
import db
import hashlib
import datetime
import matchDetailCrawler
from math import floor

logger = logging.getLogger()

def handler(event, context):
  events = json.loads(event)
  if events.get('date'):
    for date in events.get('date'):
      crawl(date)
  else:
    today = datetime.date.today()
    crawl(today.isoformat())
    yesterday = today - datetime.timedelta(days=1)
    crawl(yesterday.isoformat())
  
  return 'Done'

def crawl(date):
  conn = db.getConnection()

  now = floor(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
  url = 'https://i.sporttery.cn/wap/fb_match_list/get_fb_match_result/?format=json&date=%s&_=%d' % (date, now)
  
  try:
    # 抓取赛事数据
    req = requests.get(url)
    resultText = req.text
    h = hashlib.sha256()
    h.update(resultText.encode())
    sha256 = h.hexdigest()

    # 赛事数据没有更新的话直接结束
    with conn.cursor() as cursor:
      cursor.execute('SELECT `id` FROM `crawlerlog` WHERE `date` = %s AND `sha256` = %s', (date, sha256))
      dbResult = cursor.fetchone()
      if dbResult != None:
        logger.info('No updated data')
        return 'Done'

    result = json.loads(resultText)

    if result['data']:
      if result['data']['result']:
        for value in result['data']['result']:

          logger.info(value)
          # 保存赛事基本数据
          row = dict()
          matchId = value['id']
          matchStatus = value['match_status']
          half = value['half']
          final = value['final']

          matchDetailCrawler.crawl(matchId)
          with conn.cursor() as cursor:
            sql = 'UPDATE `matchinfo` SET matchStatus = %s, half = %s, final = %s WHERE matchId = %s AND matchStatus IS NULL'
            logger.info((matchStatus, half, final, matchId))
            cursor.execute(sql, (matchStatus, half, final, matchId))

    # 保存本次抓取日志
    with conn.cursor() as cursor:
      cursor.execute('INSERT INTO `crawlerlog` (`date`, `sha256`, `content`) VALUES (%s, %s, %s)', (date, sha256, resultText))
    conn.commit()

    return 'Done!'
  except Exception as e:
    logger.error(e)
  finally:
    conn.close()
