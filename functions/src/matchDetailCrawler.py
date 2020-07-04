# -*- coding: utf-8 -*-
import logging
import json
import requests
import db
import hashlib
import datetime
from math import floor

logger = logging.getLogger()

weekdays = dict({
  '一': 0,
  '二': 1,
  '三': 2,
  '四': 3,
  '五': 4,
  '六': 5,
  '日': 6
})

def handler(event, context):
  events = json.loads(event)
  if events.get('matchId'):
    for matchId in events.get('matchId'):
      crawl(matchId)
  else:
    conn = db.getConnection()
    with conn.cursor() as cursor:
      cursor.execute('SELECT `matchId` FROM `matchinfo` WHERE `matchStatus` IS NULL')
      rows = cursor.fetchall()
      for row in rows:
        crawl(row['matchId'])

  return 'Done'

def crawl(matchId, matchPeriod = None):
  conn = db.getConnection()

  now = floor(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)
  
  try:
    # 抓取赛事基本信息
    url = 'https://i.sporttery.cn/api/fb_match_info/get_match_info?mid=%s&_=%d' % (matchId, now)
    req = requests.get(url)
    result = req.json()

    if result.get('result'):
      value = result.get('result')
      if matchPeriod == None:
        matchDay = weekdays[value['s_num'][1]]
        logger.info(matchDay)
        matchDateTime = datetime.datetime.strptime('%s %s +0800' % (value['date_cn'], value['time_cn']), '%Y-%m-%d %H:%M:%S %z')
        logger.info(matchDateTime)
        matchPeriodDate = matchDateTime.date()
        while matchPeriodDate.weekday() > matchDay:
          matchPeriodDate -= datetime.timedelta(days=1)
        matchPeriod = matchPeriodDate.isoformat()

      row = dict()
      row['matchId'] = matchId
      row['league'] = value['l_cn']
      row['leagueAbbr'] = value['l_cn_abbr']
      row['leagueId'] = value['l_id_dc']
      row['hostTeam'] = value['h_cn']
      row['hostTeamAbbr'] = value['h_cn_abbr']
      row['hostTeamId'] = value['h_id_dc']
      row['hostTeamOrder'] = '[%s%s]' % (value['l_cn_abbr'], value['table_h'])
      row['visitingTeam'] = value['a_cn']
      row['visitingTeamAbbr'] = value['a_cn_abbr']
      row['visitingTeamId'] = value['a_id_dc']
      row['visitingTeamOrder'] = '[%s%s]' % (value['l_cn_abbr'], value['table_a'])
      row['matchPeriod'] = matchPeriod
      row['number'] = value['s_num']
      row['saleStopTime'] = floor(datetime.datetime.timestamp(matchDateTime) * 1000)
      logger.info(row)

      with conn.cursor() as cursor:
        fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
        valuesStr = ', '.join([] + ['%s'] * len(row))
        sql = 'INSERT IGNORE INTO `matchinfo` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
        cursor.execute(sql, tuple(row.values()))


    # 抓取赛事投注数据
    url = 'https://i.sporttery.cn/api/fb_match_info/get_pool_rs/?mid=%s&_=%d' % (matchId, now)
    req = requests.get(url)
    result = req.json()

    if result.get('result'):
      if result['result'].get('odds_list'):
        if result['result']['odds_list'].get('had'):
          value = result['result']['odds_list'].get('had')
          row = dict()
          row['matchId'] = matchId
          row['isSingle'] = value['single']
          for tmpValue in value['odds']:
            row['releaseTime'] = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (tmpValue['date'], tmpValue['time']), '%Y-%m-%d %H:%M:%S %z')) * 1000)
            row['win'] = tmpValue['h']
            row['level'] = tmpValue['d']
            row['lose'] = tmpValue['a']
            logger.info(row)

            with conn.cursor() as cursor:
              fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
              valuesStr = ', '.join([] + ['%s'] * len(row))
              sql = 'INSERT IGNORE INTO `spfodds` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
              cursor.execute(sql, tuple(row.values()))

        if result['result']['odds_list'].get('hhad'):
          value = result['result']['odds_list'].get('hhad')
          row = dict()
          row['matchId'] = matchId
          row['isLetSingle'] = value['single']
          row['letCount'] = value['goalline']
          for tmpValue in value['odds']:
            row['releaseTime'] = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (tmpValue['date'], tmpValue['time']), '%Y-%m-%d %H:%M:%S %z')) * 1000)
            row['letWin'] = tmpValue['h']
            row['letLevel'] = tmpValue['d']
            row['letLose'] = tmpValue['a']
            logger.info(row)

            with conn.cursor() as cursor:
              fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
              valuesStr = ', '.join([] + ['%s'] * len(row))
              sql = 'INSERT IGNORE INTO `rqspfodds` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
              cursor.execute(sql, tuple(row.values()))

        if result['result']['odds_list'].get('crs'):
          value = result['result']['odds_list'].get('crs')
          row = dict()
          row['matchId'] = matchId
          for tmpValue in value['odds']:
            row['releaseTime'] = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (tmpValue['date'], tmpValue['time']), '%Y-%m-%d %H:%M:%S %z')) * 1000)
            row['zeroToZero'] = tmpValue['0000']
            row['zeroToOne'] = tmpValue['0001']
            row['zeroToTwo'] = tmpValue['0002']
            row['zeroToThree'] = tmpValue['0003']
            row['zeroToFour'] = tmpValue['0004']
            row['zeroToFive'] = tmpValue['0005']
            row['oneToZero'] = tmpValue['0100']
            row['oneToOne'] = tmpValue['0101']
            row['oneToTwo'] = tmpValue['0102']
            row['oneToThree'] = tmpValue['0103']
            row['oneToFour'] = tmpValue['0104']
            row['oneToFive'] = tmpValue['0105']
            row['twoToZero'] = tmpValue['0200']
            row['twoToOne'] = tmpValue['0201']
            row['twoToTwo'] = tmpValue['0202']
            row['twoToThree'] = tmpValue['0203']
            row['twoToFour'] = tmpValue['0204']
            row['twoToFive'] = tmpValue['0205']
            row['threeToZero'] = tmpValue['0300']
            row['threeToOne'] = tmpValue['0301']
            row['threeToTwo'] = tmpValue['0302']
            row['threeToThree'] = tmpValue['0303']
            row['fourToZero'] = tmpValue['0400']
            row['fourToOne'] = tmpValue['0401']
            row['fourToTwo'] = tmpValue['0402']
            row['fiveToZero'] = tmpValue['0500']
            row['fiveToOne'] = tmpValue['0501']
            row['fiveToTwo'] = tmpValue['0502']
            row['winOther'] = tmpValue['-1-h']
            row['levelOther'] = tmpValue['-1-d']
            row['loseOther'] = tmpValue['-1-a']
            logger.info(row)

            with conn.cursor() as cursor:
              fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
              valuesStr = ', '.join([] + ['%s'] * len(row))
              sql = 'INSERT IGNORE INTO `bfodds` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
              cursor.execute(sql, tuple(row.values()))

        if result['result']['odds_list'].get('hafu'):
          value = result['result']['odds_list'].get('hafu')
          row = dict()
          row['matchId'] = matchId
          for tmpValue in value['odds']:
            row['releaseTime'] = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (tmpValue['date'], tmpValue['time']), '%Y-%m-%d %H:%M:%S %z')) * 1000)
            row['winWin'] = tmpValue['hh']
            row['winLevel'] = tmpValue['hd']
            row['winLose'] = tmpValue['ha']
            row['levelWin'] = tmpValue['dh']
            row['levelLevel'] = tmpValue['dd']
            row['levelLose'] = tmpValue['da']
            row['loseWin'] = tmpValue['ah']
            row['loseLevel'] = tmpValue['ad']
            row['loseLose'] = tmpValue['aa']
            logger.info(row)

            with conn.cursor() as cursor:
              fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
              valuesStr = ', '.join([] + ['%s'] * len(row))
              sql = 'INSERT IGNORE INTO `bqcodds` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
              cursor.execute(sql, tuple(row.values()))

        if result['result']['odds_list'].get('ttg'):
          value = result['result']['odds_list'].get('ttg')
          row = dict()
          row['matchId'] = matchId
          for tmpValue in value['odds']:
            row['releaseTime'] = floor(datetime.datetime.timestamp(datetime.datetime.strptime('%s %s +0800' % (tmpValue['date'], tmpValue['time']), '%Y-%m-%d %H:%M:%S %z')) * 1000)
            row['zero'] = tmpValue['s0']
            row['one'] = tmpValue['s1']
            row['two'] = tmpValue['s2']
            row['three'] = tmpValue['s3']
            row['four'] = tmpValue['s4']
            row['five'] = tmpValue['s5']
            row['six'] = tmpValue['s6']
            row['seven'] = tmpValue['s7']
            logger.info(row)

            with conn.cursor() as cursor:
              fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
              valuesStr = ', '.join([] + ['%s'] * len(row))
              sql = 'INSERT IGNORE INTO `zjqodds` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
              cursor.execute(sql, tuple(row.values()))

    conn.commit()

    return 'Done!'
  except Exception as e:
    logger.error(e)
  finally:
    logger.info('finally')
    conn.close()
