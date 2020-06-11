import logging
import pymysql
import os
import sys
import acm
import json

logger = logging.getLogger()

ACM_ENDPOINT = "addr-hz-internal.edas.aliyun.com"
ACM_NAMESPACE = "9a995f03-f355-4335-bc68-15fd9aa1a6b8"
ACM_DATA_ID= "db_config"
ACM_GROUP= "sporttery"
AK = os.environ.get('ALIYUN_AK')
SK = os.environ.get('ALIYUN_SK')

dbConfig = None

def getDbConfig():
  global dbConfig
  if dbConfig == None:
    acmClient = acm.ACMClient(ACM_ENDPOINT, ACM_NAMESPACE, AK, SK)
    dbConfig = json.loads(acmClient.get(ACM_DATA_ID, ACM_GROUP))
  return dbConfig

def getConnection():
  try:
    conn = pymysql.connect(
      host=getDbConfig()['host'],
      port=getDbConfig()['port'],
      user=getDbConfig()['username'],
      passwd=getDbConfig()['password'],
      db=getDbConfig()['name'],
      connect_timeout=5)
    return conn
  except Exception as e:
    logger.error(e)
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()