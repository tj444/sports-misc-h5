# -*- coding: utf-8 -*-

import sys
import logging
import json
import db
from datetime import datetime, timedelta
from math import floor
from utils import *

logger = logging.getLogger()

def handler(environ, start_response):
  try:
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
  except (ValueError):
    request_body_size = 0
  request_body = environ['wsgi.input'].read(request_body_size)
  params = json.loads(request_body)

  if not (params.get('matchNumber')):
    return http400(start_response)

  matchNumber = params.get('matchNumber')

  conn = db.getConnection()

  try:
    fromTime = floor(datetime.timestamp(datetime.now() - timedelta(days=1)) * 1000)
    # 根据 matchNumber 查询赛事，查询范围为自24小时前起
    with conn.cursor() as cursor:
      cursor.execute('SELECT `matchId`, `number`, `saleStopTime` FROM `matchinfo` WHERE `saleStopTime` > %s AND `number` = %s', (fromTime, matchNumber))
      dbResult = cursor.fetchone()
      if dbResult:
        resp = dict()
        resp['status'] = 0
        resp['resultTime'] = dbResult.get('saleStopTime') + 3600000 * 3
        return http200(start_response, resp)
      else:
        resp = dict()
        resp['status'] = 404
        return http200(start_response, resp)

  except Exception as e:
    logger.error(e)
    logger.error(sys.exc_info()[2])
    return http500(start_response)
  finally:
    logger.info('finally')
    conn.close()