# -*- coding: utf-8 -*-
import logging
import json
import requests
import db
import datetime
# import matchDetailCrawler
from math import floor
from utils import sha256Sum

logger = logging.getLogger()
CRAWLER_LOG_TYPE = 'get_match_list'

def handler(event, context):
  today = datetime.date.today()
  crawl(today.isoformat())
  
  return 'Done'

def crawl(date):
  conn = db.getConnection()

  url = 'https://i.sporttery.cn/api/match_live_2/get_match_list'
  
  try:
    # 抓取赛事数据
    req = requests.get(url)
    resultText = req.text
    resultText = resultText.split(' ')[-1][:-1]
    sha256 = sha256Sum(resultText)

    # 赛事数据没有更新的话直接结束
    with conn.cursor() as cursor:
      cursor.execute('SELECT `id` FROM `crawlerlog` WHERE `date` = %s AND `type` = %s AND `sha256` = %s', (date, CRAWLER_LOG_TYPE, sha256))
      dbResult = cursor.fetchone()
      if dbResult != None:
        logger.info('No updated data')
        return 'Done'

    result = json.loads(resultText)

    if len(result.keys()) > 0:
      for value in result.values():
        logger.info(value)
        # 保存赛事基本数据
        row = dict()
        row['matchId'] = value['m_id']
        row['matchStatus'] = value['status']
        if (value['fs_h']):
          row['hostFinalScore'] = value['fs_h']
        if (value['fs_a']):
          row['visitingFinalScore'] = value['fs_a']
        if (value['hts_h']):
          row['hostHalfScore'] = value['hts_h']
        if (value['hts_a']):
          row['visitingHalfScore'] = value['hts_a']
        if value['status'] == 'Played':
          row['result'] = ','.join(calcResult(value))

        # matchDetailCrawler.crawl(matchId)
        with conn.cursor() as cursor:
          fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
          updateStr = ', '.join(map(lambda x: '`' + x + '`=VALUES(`' + x + '`)', row.keys()))
          valuesStr = ', '.join([] + ['%s'] * len(row))
          sql = 'INSERT INTO `matchstatus` (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s' % (fieldsStr, valuesStr, updateStr)
          logger.info('sql: ' + sql)
          cursor.execute(sql, tuple(row.values()))

    # 保存本次抓取日志
    with conn.cursor() as cursor:
      cursor.execute('INSERT INTO `crawlerlog` (`date`, `type`, `sha256`, `content`) VALUES (%s, %s, %s, %s)', (date, CRAWLER_LOG_TYPE, sha256, resultText))
    conn.commit()

    return 'Done!'
  except Exception as e:
    logger.error(e)
  finally:
    conn.close()

def calcResult(matchStatus):
  results = []
  hostFinalScore = int(matchStatus.get('fs_h'))
  visitingFinalScore = int(matchStatus.get('fs_a'))
  hostHalfScore = int(matchStatus.get('hts_h'))
  visitingHalfScore = int(matchStatus.get('hts_a'))
  letCount = int(matchStatus.get('goalline'))
  hostLetScore = hostFinalScore + letCount

  scoreResults = dict({
    '0:0':'zeroToZero',
    '0:1':'zeroToOne',
    '0:2':'zeroToTwo',
    '0:3':'zeroToThree',
    '0:4':'zeroToFour',
    '0:5':'zeroToFive',
    '1:0':'oneToZero',
    '1:1':'oneToOne',
    '1:2':'oneToTwo',
    '1:3':'oneToThree',
    '1:4':'oneToFour',
    '1:5':'oneToFive',
    '2:0':'twoToZero',
    '2:1':'twoToOne',
    '2:2':'twoToTwo',
    '2:3':'twoToThree',
    '2:4':'twoToFour',
    '2:5':'twoToFive',
    '3:0':'threeToZero',
    '3:1':'threeToOne',
    '3:2':'threeToTwo',
    '3:3':'threeToThree',
    '4:0':'fourToZero',
    '4:1':'fourToOne',
    '4:2':'fourToTwo',
    '5:0':'fiveToZero',
    '5:1':'fiveToOne',
    '5:2':'fiveToTwo'
  })

  totalScoreResults = dict({
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven'
  })

  finalResult = compareScore(hostFinalScore, visitingFinalScore)
  results.append(finalResult)
  
  if letCount != 0:
    letResult = 'let' + compareScore(hostLetScore, visitingFinalScore).capitalize()
    results.append(letResult)
  
  finalScore = '%d:%d' % (hostFinalScore, visitingFinalScore)
  if scoreResults.get(finalScore):
    results.append(scoreResults.get(finalScore))
  else:
    results.append(finalResult + 'Other')
  
  halfResult = compareScore(hostHalfScore, visitingHalfScore) + finalResult.capitalize()
  results.append(halfResult)

  totalScore = hostFinalScore + visitingFinalScore
  if totalScoreResults.get(totalScore):
    results.append(totalScoreResults.get(totalScore))
  else:
    results.append(totalScoreResults.get(7))
  
  return results

def compareScore(hostScore, visitingScore):
  if hostScore > visitingScore:
    return 'win'
  elif hostScore == visitingScore:
    return 'level'
  else:
    return 'lose'
