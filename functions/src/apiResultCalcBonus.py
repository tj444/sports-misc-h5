# -*- coding: utf-8 -*-

import traceback
import logging
import json
import db
from itertools import combinations
from decimal import *
from utils import *

D = Decimal
logger = logging.getLogger()

mxnOptions = {
  'single': [1],
  '2x1': [2],
  '2x3': [1, 2],
  '3x1': [3],
  '3x3': [2],
  '3x4': [2, 3],
  '3x6': [1, 2],
  '3x7': [1, 2, 3],
  '4x1': [4],
  '4x4': [3],
  '4x5': [3, 4],
  '4x6': [2],
  '4x10': [1, 2],
  '4x11': [2, 3, 4],
  '4x14': [1, 2, 3],
  '4x15': [1, 2, 3, 4],
  '5x1': [5],
  '5x5': [4],
  '5x6': [5, 6],
  '5x10': [2],
  '5x15': [1, 2],
  '5x16': [3, 4, 5],
  '5x20': [2, 3],
  '5x25': [1, 2, 3],
  '5x26': [2, 3, 4, 5],
  '5x30': [1, 2, 3, 4],
  '5x31': [1, 2, 3, 4, 5],
  '6x1': [6],
  '6x6': [5],
  '6x7': [5, 6],
  '6x15': [2],
  '6x20': [3],
  '6x21': [1, 2],
  '6x22': [4, 5, 6],
  '6x35': [2, 3],
  '6x41': [1, 2, 3],
  '6x42': [3, 4, 5, 6],
  '6x50': [2, 3, 4],
  '6x56': [1, 2, 3, 4],
  '6x57': [2, 3, 4, 5, 6],
  '6x62': [1, 2, 3, 4, 5],
  '6x63': [1, 2, 3, 4, 5, 6],
  '7x1': [7],
  '7x7': [6],
  '7x8': [6, 7],
  '7x21': [5],
  '7x35': [4],
  '7x120': [2, 3, 4, 5, 6, 7],
  '7x127': [1, 2, 3, 4, 5, 6, 7],
  '8x1': [8],
  '8x8': [7],
  '8x9': [7, 8],
  '8x28': [6],
  '8x56': [5],
  '8x70': [4],
  '8x247': [2, 3, 4, 5, 6, 7, 8],
  '8x255': [1, 2, 3, 4, 5, 6, 7, 8]
}

maxBonus = {
  1: D(100000),
  2: D(200000),
  3: D(200000),
  4: D(500000),
  5: D(500000),
  6: D(1000000),
  7: D(1000000),
  8: D(1000000)
}


def handler(environ, start_response):
  try:
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
  except (ValueError):
    request_body_size = 0
  request_body = environ['wsgi.input'].read(request_body_size)
  params = json.loads(request_body)

  if not (params.get('betting') and params.get('options') and params.get('multiple') and params.get('bettingTime')):
    return http400(start_response)
  
  bettingTime = params.get('bettingTime')
  options = params.get('options')
  betting = params.get('betting')
  multiple = params.get('multiple')
  for option in options:
    if not option in mxnOptions.keys():
      return http400(start_response)

  matchNumbers = []
  for matchBetting in betting:
    matchNumbers.append(matchBetting.get('matchNumber'))
  
  conn = db.getConnection()

  logger.info('params: {}'.format(params))

  try:
    matchIds = []
    matchInfoById = dict()
    matchInfoByNumber = dict()
    resultById = dict()
    oddsById = dict()
    
    # 根据 matchNumber 查询赛事，查询范围为自投注时间起 4 天内
    with conn.cursor() as cursor:
      # 查询赛事基本信息
      cursor.execute('SELECT `matchId`, `number`, `saleStopTime` FROM `matchinfo` WHERE `saleStopTime` BETWEEN %s AND %s AND `number` IN %s', (bettingTime, bettingTime + 86400000 * 4, matchNumbers))
      matches = cursor.fetchall()
      if len(matches) < len(matchNumbers):
        for mi in matches:
          matchNumbers.remove(mi.get('number'))
        resp = dict()
        resp['status'] = 101
        resp['message'] = 'Invalid matchNumbers: ' + ', '.join(matchNumbers)
        return http200(start_response, resp)
      else:
        for mi in matches:
          matchInfoById[mi.get('matchId')] = mi
          matchInfoByNumber[mi.get('number')] = mi
          matchIds.append(mi.get('matchId'))

      logger.info('matchIds: {}'.format(matchIds))
      logger.info('matchInfoById: {}'.format(matchInfoById))
      logger.info('matchInfoByNumber: {}'.format(matchInfoByNumber))

      # 查询赛事状态
      cursor.execute('SELECT `matchId`, `matchStatus`, `result` FROM `matchstatus` WHERE `matchId` IN %(matchIds)s AND `result` IS NOT NULL', {'matchIds': matchIds})
      matchStatuses = cursor.fetchall()
      logger.info('matchStatuses: {}'.format(matchStatuses))
      for ms in matchStatuses:
        resultById[ms.get('matchId')] = ms.get('result').split(',')
        matchIds.remove(ms.get('matchId'))

      if len(matchIds) > 0:
        resp = dict()
        resp['status'] = 100
        resp['message'] = 'The following matches are not finished: ' + ', '.join(map(lambda x: matchInfoById.get(x).get('number'), matchIds))
        return http200(start_response, resp)

      logger.info('resultById: {}'.format(resultById))
    
    # 猜中比赛的赔率，计算奖金只需要这些
    odds = []
    for matchBetting in betting:
      matchId = matchInfoByNumber.get(matchBetting.get('matchNumber')).get('matchId')
      resultSet = set(matchBetting.get('bettingItems')) & set(resultById.get(matchId))
      if resultSet:
        odds.append(getOdds(matchId, resultSet.pop(), bettingTime))
      else:
        odds.append("0")

    logger.info('odds: {}'.format(odds))

    # 终于开始算奖了，注意，算钱的时候一定要用 Decimal，除非都是整数
    totalBonus = D(0)
    for option in options:
      if option == 'single':
        for o in odds:
          totalBonus += D(2) * D(o)
      else:
        m = int(option.split('x')[0])
        ns = mxnOptions.get(option)
        for comb0 in combinations(odds, m):
          for n in ns:
            for comb1 in combinations(comb0, n):
              bonus = D(2)
              for v in comb1:
                bonus *= D(v)
              bonus = roundBonus(bonus)
              totalBonus += min(bonus, maxBonus.get(n))

    totalBonus *= D(multiple)

    resp = dict()
    resp['status'] = 0
    resp['bonus'] = str(totalBonus)

    return http200(start_response, resp)

  except Exception as e:
    logger.error(traceback.format_exc())
    return http500(start_response)
  finally:
    logger.info('finally')
    conn.close()

def getOdds(matchId, item, saleTime):
  conn = db.getConnection()
  try:
    if item in ('win','level','lose'):
      sql = "SELECT `{item}` FROM `spfodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1"
    elif item in ('letWin','letLevel','letLose'):
      sql = "SELECT `{item}` FROM `rqspfodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1"
    elif item in ('zeroToZero','zeroToOne','zeroToTwo','zeroToThree','zeroToFour','zeroToFive','oneToZero','oneToOne','oneToTwo','oneToThree','oneToFour','oneToFive','twoToZero','twoToOne','twoToTwo','twoToThree','twoToFour','twoToFive','threeToZero','threeToOne','threeToTwo','threeToThree','fourToZero','fourToOne','fourToTwo','fiveToZero','fiveToOne','fiveToTwo','winOther','levelOther','loseOther'):
      sql = "SELECT `{item}` FROM `bfodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1"
    elif item in ('winWin','winLevel','winLose','levelWin','levelLevel','levelLose','loseWin','loseLevel','loseLose'):
      sql = "SELECT `{item}` FROM `bqcodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1"
    elif item in ('zero','one','two','three','four','five','six','seven'):
      sql = "SELECT `{item}` FROM `zjqodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1"
    
    sql = sql.format(item=item, matchId=matchId, saleTime=saleTime)

    with conn.cursor() as cursor:
      # 查询赛事基本信息
      cursor.execute(sql)
      dbResult = cursor.fetchone()
      return dbResult.get(item)
  except Exception as e:
    logger.error(traceback.format_exc())
  finally:
    conn.close()

def roundBonus(bonus):
  [m,n] = str(bonus).split('.')
  if len(n) > 2:
    if int(n[2]) < 5:
      return D('{}.{}'.format(m, n[0:2]))
    elif int(n[2]) == '5':
      if len(n) < 4 or int(n[3]) % 2 == 0:
        return D('{}.{}'.format(m, n[0:2]))
    return D('{}.{}'.format(m, n[0:2])) + D('0.01')
  else:
    return bonus
