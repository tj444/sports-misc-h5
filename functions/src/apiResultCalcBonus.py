# -*- coding: utf-8 -*-

import logging
import json
import db
import datetime
from math import floor

logger = logging.getLogger()

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
  matchNumbers = []
  for betting in params.get('betting'):
    matchNumbers.append(betting.get('matchNumber'))
  
  conn = db.getConnection()

  logger.info('params: {}'.format(params))

  try:
    matchIds = []
    matchInfoById = dict()
    matchInfoByNumber = dict()
    bettingById = dict()
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
    
    for matchId in resultById.keys():
      oddsById[matchId] = getOdds(matchId, resultById[matchId], bettingTime)

    logger.info('oddsById: {}'.format(oddsById))

    resp = dict()
    resp['status'] = 0
    resp['bonus'] = 0

    return http200(start_response, resp)

  except Exception as e:
    logger.error(e)
    return http500(start_response)
  finally:
    logger.info('finally')
    conn.close()

def getOdds(matchId, result, saleTime):
  conn = db.getConnection()
  try:
    sql = """WITH
      spf AS (SELECT `win`,`level`,`lose` FROM `spfodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1),
      rqspf AS (SELECT `letWin`,`letLevel`,`letLose` FROM `rqspfodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1),
      bf AS (SELECT `zeroToZero`,`zeroToOne`,`zeroToTwo`,`zeroToThree`,`zeroToFour`,`zeroToFive`,`oneToZero`,`oneToOne`,`oneToTwo`,`oneToThree`,`oneToFour`,`oneToFive`,`twoToZero`,`twoToOne`,`twoToTwo`,`twoToThree`,`twoToFour`,`twoToFive`,`threeToZero`,`threeToOne`,`threeToTwo`,`threeToThree`,`fourToZero`,`fourToOne`,`fourToTwo`,`fiveToZero`,`fiveToOne`,`fiveToTwo`,`winOther`,`levelOther`,`loseOther` FROM `bfodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1),
      bqc AS (SELECT `winWin`,`winLevel`,`winLose`,`levelWin`,`levelLevel`,`levelLose`,`loseWin`,`loseLevel`,`loseLose` FROM `bqcodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1),
      zjq AS (SELECT `zero`,`one`,`two`,`three`,`four`,`five`,`six`,`seven` FROM `zjqodds` WHERE `matchId` = {matchId} AND `releaseTime` < {saleTime} ORDER BY `releaseTime` DESC LIMIT 1)
      SELECT * FROM spf, rqspf, bf, bqc, zjq
    """.format(matchId=matchId, saleTime=saleTime)

    with conn.cursor() as cursor:
      # 查询赛事基本信息
      logger.info('sql: {}'.format(sql))
      cursor.execute(sql)
      dbResult = cursor.fetchone()
      logger.info('odds of {}: {}'.format(matchId, dbResult))
      odds = dict()
      for k in result:
        odds[k] = float(dbResult.get(k, 0))
      return odds
  except Exception as e:
    logger.error(e)
  finally:
    conn.close()

def http400(start_response):
  status = '400 Bad Request'
  response_headers = []
  start_response(status, response_headers)
  return []

def http500(start_response):
  status = '500 Server Error1'
  response_headers = []
  start_response(status, response_headers)
  return []

def http200(start_response, data):
  status = '200 OK'
  response_headers = [('Content-type', 'application/json')]
  start_response(status, response_headers)
  return [json.dumps(data).encode()]