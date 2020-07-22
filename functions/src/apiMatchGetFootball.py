# -*- coding: utf-8 -*-

import logging
import json
import db
import datetime
from math import floor

logger = logging.getLogger()

defaultFields = dict({
  "matchId": "",
  "league": "",
  "hostTeam": "",
  "visitingTeam": "",
  "matchPeriod": "",
  "number": "",
  "printStopTime": None,
  "saleStopTime": None,
  "startTime": None,
  "stopTime": None,
  "isSpf": "",
  "isSingle": "",
  "win": "",
  "level": "",
  "lose": "",
  "isRqspf": "",
  "isLetSingle": "",
  "letCount": "",
  "letWin": "",
  "letLevel": "",
  "letLose": "",
  "isBf": "",
  "zeroToZero": "",
  "zeroToOne": "",
  "zeroToTwo": "",
  "zeroToThree": "",
  "zeroToFour": "",
  "zeroToFive": "",
  "oneToZero": "",
  "oneToOne": "",
  "oneToTwo": "",
  "oneToThree": "",
  "oneToFour": "",
  "oneToFive": "",
  "twoToZero": "",
  "twoToOne": "",
  "twoToTwo": "",
  "twoToThree": "",
  "twoToFour": "",
  "twoToFive": "",
  "threeToZero": "",
  "threeToOne": "",
  "threeToTwo": "",
  "threeToThree": "",
  "fourToZero": "",
  "fourToOne": "",
  "fourToTwo": "",
  "fiveToZero": "",
  "fiveToOne": "",
  "fiveToTwo": "",
  "winOther": "",
  "levelOther": "",
  "loseOther": "",
  "isBqc": "",
  "winWin": "",
  "winLevel": "",
  "winLose": "",
  "levelWin": "",
  "levelLevel": "",
  "levelLose": "",
  "loseWin": "",
  "loseLevel": "",
  "loseLose": "",
  "isZjq": "",
  "zero": "",
  "one": "",
  "two": "",
  "three": "",
  "four": "",
  "five": "",
  "six": "",
  "seven": ""
})

def handler(environ, start_response):
  conn = db.getConnection()
  data = []
  now = floor(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)

  try :
    sql = """SELECT `matchinfo`.`matchId`,`leagueAbbr` as `league`,`hostTeamAbbr` as `hostTeam`,`visitingTeamAbbr` as `visitingTeam`,`matchPeriod`,`number`,`printStopTime`,`saleStopTime`,`startTime`,`stopTime`,
    `isSpf`,`isSingle`,`win`,`level`,`lose`,
    `isRqspf`,`isLetSingle`,`letCount`,`letWin`,`letLevel`,`letLose`,
    `isBf`,`zeroToZero`,`zeroToOne`,`zeroToTwo`,`zeroToThree`,`zeroToFour`,`zeroToFive`,`oneToZero`,`oneToOne`,`oneToTwo`,`oneToThree`,`oneToFour`,`oneToFive`,`twoToZero`,`twoToOne`,`twoToTwo`,`twoToThree`,`twoToFour`,`twoToFive`,`threeToZero`,`threeToOne`,`threeToTwo`,`threeToThree`,`fourToZero`,`fourToOne`,`fourToTwo`,`fiveToZero`,`fiveToOne`,`fiveToTwo`,`winOther`,`levelOther`,`loseOther`,
    `isBqc`,`winWin`,`winLevel`,`winLose`,`levelWin`,`levelLevel`,`levelLose`,`loseWin`,`loseLevel`,`loseLose`,
    `isZjq`,`zero`,`one`,`two`,`three`,`four`,`five`,`six`,`seven`
    FROM `matchinfo`
    LEFT OUTER JOIN `spf` ON `matchinfo`.`matchId` = `spf`.`matchId`
    LEFT OUTER JOIN `rqspf` ON `matchinfo`.`matchId` = `rqspf`.`matchId`
    LEFT OUTER JOIN `bf` ON `matchinfo`.`matchId` = `bf`.`matchId`
    LEFT OUTER JOIN `bqc` ON `matchinfo`.`matchId` = `bqc`.`matchId`
    LEFT OUTER JOIN `zjq` ON `matchinfo`.`matchId` = `zjq`.`matchId`
    WHERE saleStopTime >= %s
    """
    with conn.cursor() as cursor:
      cursor.execute(sql, (now))
      dbResult = cursor.fetchall()
      if len(dbResult) > 0:
        for row in dbResult:
          matchData = {**defaultFields, **row, 'matchPeriod': row.get('matchPeriod').isoformat()}
          data.append(matchData)
  finally:
    conn.close()

  status = '200 OK'
  response_headers = [('Content-type', 'application/json')]
  start_response(status, response_headers)
  return [json.dumps(data).encode()]