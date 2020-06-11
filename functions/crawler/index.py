# -*- coding: utf-8 -*-
import logging
import json
import requests
import db
import hashlib
import datetime

logger = logging.getLogger()

def handler(event, context):
  url = 'https://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]=hhad&poolcode[]=had&poolcode[]=crs&poolcode[]=ttg&poolcode[]=hafu'
  req = requests.get(url)
  resultText = req.text
  h = hashlib.sha256()
  h.update(resultText.encode())
  sha256 = h.hexdigest()

  today = datetime.date.today().isoformat()

  conn = db.getConnection()

  try:
    with conn.cursor() as cursor:
      cursor.execute('SELECT `id` FROM `crawlerlog` WHERE `date` = %s AND `sha256` = %s', (today, sha256))
      dbResult = cursor.fetchone()
      if dbResult != None:
        logger.info('No updated data')
        return 'Done'

    result = json.loads(resultText)

    if result['data']:
      for value in result['data'].values():
        matchId = value['id']

        row = dict()
        row['matchId'] = matchId
        row['league'] = value['l_cn']
        row['hostTeam'] = value['h_cn']
        row['visitingTeam'] = value['a_cn']
        row['matchPeriod'] = value['b_date']
        row['number'] = value['num']

        with conn.cursor() as cursor:
          fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
          valuesStr = ', '.join([] + ['%s'] * len(row))
          sql = 'REPLACE INTO `matchinfo` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
          cursor.execute(sql, tuple(row.values()))

        if value.get('had'):
          tmpValue = value['had']
          row = dict()
          row['matchId'] = matchId
          row['isSpf'] = tmpValue['p_status']
          row['isSingle'] = tmpValue['single']
          row['win'] = tmpValue['h']
          row['level'] = tmpValue['d']
          row['lose'] = tmpValue['a']

          with conn.cursor() as cursor:
            fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
            valuesStr = ', '.join([] + ['%s'] * len(row))
            sql = 'REPLACE INTO `spf` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
            cursor.execute(sql, tuple(row.values()))

        if value.get('hhad'):
          tmpValue = value['hhad']
          row = dict()
          row['matchId'] = matchId
          row['isRqspf'] = tmpValue['p_status']
          row['isLetSingle'] = tmpValue['single']
          row['letCount'] = tmpValue['fixedodds']
          row['letWin'] = tmpValue['h']
          row['letLevel'] = tmpValue['d']
          row['letLose'] = tmpValue['a']

          with conn.cursor() as cursor:
            fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
            valuesStr = ', '.join([] + ['%s'] * len(row))
            sql = 'REPLACE INTO `rqspf` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
            cursor.execute(sql, tuple(row.values()))

        if value.get('crs'):
          tmpValue = value['crs']
          row = dict()
          row['matchId'] = matchId
          row['isBf'] = tmpValue['p_status']
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
          row['fourToZero'] = tmpValue['0400']
          row['fourToOne'] = tmpValue['0401']
          row['fourToTwo'] = tmpValue['0402']
          row['fiveToZero'] = tmpValue['0500']
          row['fiveToOne'] = tmpValue['0501']
          row['fiveToTwo'] = tmpValue['0502']
          row['winOther'] = tmpValue['-1-h']
          row['levelOther'] = tmpValue['-1-d']
          row['loseOther'] = tmpValue['-1-a']

          with conn.cursor() as cursor:
            fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
            valuesStr = ', '.join([] + ['%s'] * len(row))
            sql = 'REPLACE INTO `bf` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
            cursor.execute(sql, tuple(row.values()))

        if value.get('hafu'):
          tmpValue = value['hafu']
          row = dict()
          row['matchId'] = matchId
          row['isBqc'] = tmpValue['p_status']
          row['winWin'] = tmpValue['hh']
          row['winLevel'] = tmpValue['hd']
          row['winLose'] = tmpValue['ha']
          row['levelWin'] = tmpValue['dh']
          row['levelLevel'] = tmpValue['dd']
          row['levelLose'] = tmpValue['da']
          row['loseWin'] = tmpValue['ah']
          row['loseLevel'] = tmpValue['ad']
          row['loseLose'] = tmpValue['aa']

          with conn.cursor() as cursor:
            fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
            valuesStr = ', '.join([] + ['%s'] * len(row))
            sql = 'REPLACE INTO `bqc` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
            cursor.execute(sql, tuple(row.values()))

        if value.get('ttg'):
          tmpValue = value['ttg']
          row = dict()
          row['matchId'] = matchId
          row['isZjq'] = tmpValue['p_status']
          row['zero'] = tmpValue['s0']
          row['one'] = tmpValue['s1']
          row['two'] = tmpValue['s2']
          row['three'] = tmpValue['s3']
          row['four'] = tmpValue['s4']
          row['five'] = tmpValue['s5']
          row['six'] = tmpValue['s6']
          row['seven'] = tmpValue['s7']

          with conn.cursor() as cursor:
            fieldsStr = ', '.join(map(lambda x: '`' + x + '`', row.keys()))
            valuesStr = ', '.join([] + ['%s'] * len(row))
            sql = 'REPLACE INTO `zjq` (%s) VALUES (%s)' % (fieldsStr, valuesStr)
            cursor.execute(sql, tuple(row.values()))

    with conn.cursor() as cursor:
      cursor.execute('INSERT INTO `crawlerlog` (`date`, `sha256`, `content`) VALUES (%s, %s, %s)', (today, sha256, resultText))
    conn.commit()

    return 'Done!'
  finally:
    conn.close()