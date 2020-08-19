# -*- coding: utf-8 -*-
import logging
import json
import requests
import db
import hashlib
import datetime

logger = logging.getLogger()

CRAWLER_LOG_TYPE = '500_get_match_info'

def handler(event, context):
  forceUpdate = False
  try:
    evt = json.loads(event)
    forceUpdate = evt.get('forceUpdate') == True
  except Exception as e:
    logger.error(e)

  conn = db.getConnection()

  try:
    today = datetime.date.today().isoformat()
    startTime = None
    stopTime = None

    # 查询售卖时间
    with conn.cursor() as cursor:
      cursor.execute('SELECT `startTime`, `stopTime` FROM `saletime` WHERE `date` = %s', (today))
      dbResult = cursor.fetchone()
      if dbResult != None:
        now = datetime.datetime.timestamp(datetime.datetime.now()) * 1000
        startTime = dbResult['startTime']
        stopTime = dbResult['stopTime']

    # 抓取赛事数据
    url = 'https://evs.500.com/esinfo/lotinfo/lot_info?lotid=46&lottype=huntou&page=1&pagesize=100&webviewsource=touch&platform=touch'
    req = requests.get(url)
    resultText = req.text
    h = hashlib.sha256()
    h.update(resultText.encode())
    sha256 = h.hexdigest()
    logger.info('sha256: ' + sha256)

    if not forceUpdate:
      # 赛事数据没有更新的话直接结束
      with conn.cursor() as cursor:
        cursor.execute('SELECT `id` FROM `crawlerlog` WHERE `date` = %s AND `type` = %s AND `sha256` = %s', (today, CRAWLER_LOG_TYPE, sha256))
        dbResult = cursor.fetchone()
        if dbResult != None:
          logger.info('No updated data')
          return 'Done'

    result = json.loads(resultText)

    if result.get('status') == '100' and result['data']:
      matches = dict()
      matchIds = list(map(lambda x: int(x['mdata']['id']), result['data']))
      with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM `matchinfo` WHERE `matchId` IN %s', ([matchIds]))
        dbResult = cursor.fetchall()
        if dbResult:
          for m in dbResult:
            matches[m['matchId']] = m

      for value in result['data']:
        tmpValue = value['mdata']
        matchId = int(tmpValue['id'])

        # 保存赛事基本数据
        row = dict()
        row['matchId'] = matchId
        row['league'] = tmpValue['simpleleague']
        row['leagueAbbr'] = tmpValue['simpleleague']
        row['hostTeam'] = tmpValue['homesxname']
        row['hostTeamAbbr'] = tmpValue['homesxname']
        row['hostTeamOrder'] = tmpValue['homestanding']
        row['visitingTeam'] = tmpValue['awaysxname']
        row['visitingTeamAbbr'] = tmpValue['awaysxname']
        row['visitingTeamOrder'] = tmpValue['awaystanding']
        row['matchPeriod'] = tmpValue['matchdate']
        row['number'] = tmpValue['matchnum']
        row['500fid'] = tmpValue['fid']
        row['saleStopTime'] = int(datetime.datetime.timestamp(datetime.datetime.strptime('{}:00 +0800'.format(tmpValue['endtime']), '%Y-%m-%d %H:%M:%S %z')) * 1000)

        with conn.cursor() as cursor:
          if not matches.get(matchId):
            fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
            valuesStr = ', '.join([] + ['%s'] * len(row))
            sql = 'INSERT INTO `matchinfo` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
            cursor.execute(sql, tuple(row.values()))
          else:
            sql = 'UPDATE `matchinfo` SET `500fid` = %s WHERE `matchId` = %s'
            cursor.execute(sql, (row['500fid'], row['matchId']))
            # sql = 'UPDATE `matchinfo` SET `500fid` = %s, `saleStopTime` = %s WHERE `matchId` = %s'
            # cursor.execute(sql, (row['500fid'], row['saleStopTime'], row['matchId']))

    # 保存本次抓取日志
    with conn.cursor() as cursor:
      cursor.execute('INSERT INTO `crawlerlog` (`date`, `type`, `sha256`, `content`) VALUES (%s, %s, %s, %s)', (today, CRAWLER_LOG_TYPE, sha256, resultText))
    conn.commit()

    return 'Done!'
  finally:
    conn.close()