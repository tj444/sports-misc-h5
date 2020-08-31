# -*- coding: utf-8 -*-
import logging
import json
import requests
import db
import hashlib
import datetime
import matchDetailCrawler
from math import floor

CRAWLER_LOG_TYPE = 'get_fb_match_result'

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

    matchInfoMap = dict()
    matchStatusMap = dict()

    result = json.loads(resultText)
    matchIds = list(map(lambda x: x['id'], result['data']['result']))
    updated = False

    # 赛事数据没有更新的话直接结束
    with conn.cursor() as cursor:
      cursor.execute('SELECT * FROM `matchinfo` WHERE `matchId` IN %s', ([matchIds]))
      dbResult = cursor.fetchall()
      if dbResult:
        for m in dbResult:
          matchInfoMap[int(m['matchId'])] = m

      cursor.execute('SELECT * FROM `matchstatus` WHERE `matchId` IN %s', ([matchIds]))
      dbResult = cursor.fetchall()
      if dbResult:
        for m in dbResult:
          matchStatusMap[int(m['matchId'])] = m

    if result['data']:
      if result['data']['result']:
        for value in result['data']['result']:

          logger.info(value)
          # 保存赛事基本数据
          row = dict()
          matchId = int(value['id'])
          matchStatus = value['match_status']
          half = value['half']
          final = value['final']

          # 仅当抓取到的状态与库中状态不一致时更新
          if matchInfoMap.get(matchId) and matchInfoMap[matchId]['matchStatus'] != matchStatus:
            updated = True
            matchDetailCrawler.crawl(matchId)
            with conn.cursor() as cursor:
              sql = 'UPDATE `matchinfo` SET matchStatus = %s, half = %s, final = %s WHERE matchId = %s'
              logger.info((matchStatus, half, final, matchId))
              cursor.execute(sql, (matchStatus, half, final, matchId))

              # 如果赛事已开奖，但赛事比分状态仍然不是已结束，则去更新赛事的比分状态
              if matchStatus in ('Final', 'Define') and not (matchStatusMap.get(matchId) and matchStatusMap[matchId]['matchStatus'] in ('Played', 'Refund')):
                updateMatchStatusToPlayed(matchId, final, half, value['fixedodds'], conn)

    if updated:
      # 保存本次抓取日志
      with conn.cursor() as cursor:
        cursor.execute('INSERT INTO `crawlerlog` (`date`, `type`, `sha256`, `content`) VALUES (%s, %s, %s, %s)', (date, CRAWLER_LOG_TYPE, sha256, resultText))
      conn.commit()

    return 'Done!'
  except Exception as e:
    logger.error(e)
  finally:
    conn.close()

def updateMatchStatusToPlayed(matchId, final, half, letCount, conn):
  row = dict()
  if final in ('无效场次', '取消'):
    row['matchId'] = matchId
    row['matchStatus'] = 'Refund'
    row['hostFinalScore'] = 0
    row['visitingFinalScore'] = 0
    row['hostHalfScore'] = 0
    row['visitingHalfScore'] = 0
  else:
    row['matchId'] = matchId
    row['matchStatus'] = 'Played'
    finalScores = final.split(':')
    row['hostFinalScore'] = int(finalScores[0])
    row['visitingFinalScore'] = int(finalScores[1])
    halfScores = half.split(':')
    row['hostHalfScore'] = int(halfScores[0])
    row['visitingHalfScore'] = int(halfScores[1])
    row['letCount'] = int(float(letCount))
    row['result'] = ','.join(calcResult(row))
    row.pop('letCount')

  with conn.cursor() as cursor:
    fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
    updateStr = ', '.join(map(lambda x: '`' + x + '`=VALUES(`' + x + '`)', row.keys()))
    valuesStr = ', '.join([] + ['%s'] * len(row))
    sql = 'INSERT INTO `matchstatus` (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s' % (fieldsStr, valuesStr, updateStr)
    logger.info('sql: ' + sql)
    cursor.execute(sql, tuple(row.values()))

def calcResult(matchStatus):
  results = []
  hostFinalScore = int(matchStatus.get('hostFinalScore'))
  visitingFinalScore = int(matchStatus.get('visitingFinalScore'))
  hostHalfScore = int(matchStatus.get('hostHalfScore'))
  visitingHalfScore = int(matchStatus.get('visitingHalfScore'))
  letCount = int(matchStatus.get('letCount'))
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
