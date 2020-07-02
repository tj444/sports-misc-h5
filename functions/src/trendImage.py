# -*- coding: utf-8 -*-

import logging
import json
import db
import datetime
import fileinput
from math import floor

logger = logging.getLogger()

resultToKey = dict({
    1: 'winOdds',
    0: 'levelOdds',
    -1: 'loseOdds'
})

resultToChinese = dict({
    1: '胜',
    0: '平',
    -1: '负'
})

oddsLevelToChinese = dict({
    'low': '低',
    'middle': '中',
    'high': '高'
})

totalScoreToChinese = dict({
    'zero': '小',
    'two': '中',
    'four': '大'
})

def handler(environ, start_response):
  conn = db.getConnection()
  now = floor(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)

  day90startTime = now - 86400000 * 90;
  day30startTime = now - 86400000 * 30;

  result = dict()

  tplFile = open("trendImage.tpl", "r")
  html = tplFile.read()

  try :
    matchData = []
    sql = """
    WITH tmptable AS (
      SELECT matchinfo.matchId, matchinfo.saleStopTime, matchinfo.number, matchinfo.hostTeamAbbr AS hostTeam, matchinfo.visitingTeamAbbr as visitingTeam, matchinfo.half, matchinfo.final, win, level, lose, 0 as letCount, releaseTime
    FROM spfodds JOIN matchinfo ON matchinfo.matchId = spfodds.matchId
    WHERE isSingle = '1' AND (matchinfo.matchStatus = 'Final' OR matchinfo.matchStatus IS NULL) AND saleStopTime > %s
      UNION ALL
      SELECT matchinfo.matchId, matchinfo.saleStopTime, matchinfo.number, matchinfo.hostTeamAbbr , matchinfo.visitingTeamAbbr, matchinfo.half, matchinfo.final, letWin, letLevel, letLose, letCount, releaseTime
    FROM rqspfodds JOIN matchinfo ON matchinfo.matchId = rqspfodds.matchId
    WHERE isLetSingle = '1' AND (matchinfo.matchStatus = 'Final' OR matchinfo.matchStatus IS NULL) AND saleStopTime > %s
    )
    SELECT * FROM tmptable ORDER BY matchId ASC, releaseTime DESC;
    """
    with conn.cursor() as cursor:
      cursor.execute(sql, (day90startTime, day90startTime))
      matchData = cursor.fetchall()
    
    alldata = preProcessData(matchData)
    miss = calcMiss(alldata)
    data = filter30day(alldata, day30startTime)
    result = dict({
      'miss': miss,
      'data': data
    })

    contentTableHtml = """
    <table>
      <thead>
            <tr>
                <th class="date" rowspan="2">日期</th>
                <th class="weekday" rowspan="2">周</th>
                <th class="match" rowspan="2">比赛</th>
                <th class="spf" rowspan="2">胜</th>
                <th class="spf" rowspan="2">平</th>
                <th class="spf" rowspan="2">负</th>
                <th class="odds" colspan="3">赔率</th>
                <th class="total" colspan="3">总进球</th>
                <th class="half" rowspan="2">半全场</th>
            </tr>
            <tr>
                <th class="odds">低赔</th>
                <th class="odds">中赔</th>
                <th class="odds">高赔</th>
                <th class="total">0-1</th>
                <th class="total">2-3</th>
                <th class="total">4-5</th>
            </tr>
        </thead>
        <tbody>
    """
    for v in data:
      contentTableHtml += '<tr>'
      contentTableHtml += '<td class="date">%s</td>' % (v['date'])
      contentTableHtml += '<td class="weekday">%s</td>' % (v['weekday'])
      hostTeam = v['hostTeam']
      if v['letCount'] != '0':
        hostTeam = '(' + v['letCount'] + ')' + hostTeam
      if v.get('finalScore'):
        contentTableHtml += '<td class="match">%s<span class="score">%s</span>%s</td>' % (hostTeam, v['finalScore'], v['visitingTeam'])
        contentTableHtml += '<td class="spf %s">%s</td>' % ('active-' + v['activeOddsLevel'] if v['letResult'] == 1 else '', v['winOdds'])
        contentTableHtml += '<td class="spf %s">%s</td>' % ('active-' + v['activeOddsLevel'] if v['letResult'] == 0 else '', v['levelOdds'])
        contentTableHtml += '<td class="spf %s">%s</td>' % ('active-' + v['activeOddsLevel'] if v['letResult'] == -1 else '', v['loseOdds'])
        contentTableHtml += '<td class="odds %s">%s</td>' % ('active-low' if v['miss']['low'] == 0 else '', '低' if v['miss']['low'] == 0 else v['miss']['low'])
        contentTableHtml += '<td class="odds %s">%s</td>' % ('active-middle' if v['miss']['middle'] == 0 else '', '中' if v['miss']['middle'] == 0 else v['miss']['middle'])
        contentTableHtml += '<td class="odds %s">%s</td>' % ('active-high' if v['miss']['high'] == 0 else '', '高' if v['miss']['high'] == 0 else v['miss']['high'])
        contentTableHtml += '<td class="total %s">%s</td>' % ('active-low' if v['miss']['zero'] == 0 else '', '小' if v['miss']['zero'] == 0 else v['miss']['zero'])
        contentTableHtml += '<td class="total %s">%s</td>' % ('active-middle' if v['miss']['two'] == 0 else '', '中' if v['miss']['two'] == 0 else v['miss']['two'])
        contentTableHtml += '<td class="total %s">%s</td>' % ('active-high' if v['miss']['four'] == 0 else '', '大' if v['miss']['four'] == 0 else v['miss']['four'])
        contentTableHtml += '<td class="half">%s</td>' % (resultToChinese.get(v['halfResult']) + resultToChinese.get(v['result']))
      else:
        contentTableHtml += '<td class="match">%s VS %s</td>' % (hostTeam, v['visitingTeam'])
        contentTableHtml += '<td class="spf">%s</td>' % (v['winOdds'])
        contentTableHtml += '<td class="spf">%s</td>' % (v['levelOdds'])
        contentTableHtml += '<td class="spf">%s</td>' % (v['loseOdds'])
        contentTableHtml += '<td class="odds">\</td>'
        contentTableHtml += '<td class="odds">\</td>'
        contentTableHtml += '<td class="odds">\</td>'
        contentTableHtml += '<td class="total">\</td>'
        contentTableHtml += '<td class="total">\</td>'
        contentTableHtml += '<td class="total">\</td>'
        contentTableHtml += '<td class="half">\</td>'
      contentTableHtml += '<tr>'
    contentTableHtml += "</tbody></table>"

    missTableHtml = """
    <table>
        <tr>
            <td rowspan="2">最高遗漏次数<br/><span class="comment">（近3个月）</span></span></td>
            <td>低赔</td>
            <td>中赔</td>
            <td>高赔</td>
            <td>0-1球</td>
            <td>2-3球</td>
            <td>4-5球</td>
        </tr>
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>
    </table>
    """ % (miss['low'], miss['middle'], miss['high'], miss['zero'], miss['two'], miss['four'])

    html = html.replace('//CONTENT_TABLE//', contentTableHtml)
    html = html.replace('//MISS_TABLE//', missTableHtml)

  finally:
    conn.close()

  status = '200 OK'
  # response_headers = [('Content-type', 'application/json')]
  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  # return [json.dumps(result).encode()]
  return [html.encode('utf-8')]

def preProcessData(matchData):
  result = dict()
  for row in matchData:
    matchId = row['matchId']
    if not result.get(matchId):
      matchInfo = dict()
      matchInfo['matchId'] = row['matchId']
      matchInfo['saleStopTime'] = row['saleStopTime']
      saleStopDateTime = datetime.datetime.fromtimestamp(row['saleStopTime'] / 1000)
      matchInfo['date'] = saleStopDateTime.strftime('%m月%d日')
      matchInfo['weekday'] = row['number'][1]
      matchInfo['hostTeam'] = row['hostTeam']
      matchInfo['visitingTeam'] = row['visitingTeam']
      matchInfo['letCount'] = row['letCount']
      matchInfo['winOdds'] = float(row['win'])
      matchInfo['levelOdds'] = float(row['level'])
      matchInfo['loseOdds'] = float(row['lose'])

      if (row['final']):
        finalScores = row['final'].split(':')
        hostFinalScore = int(finalScores[0])
        visitingFinalScore = int(finalScores[1])
        matchInfo['finalScore'] = row['final']
        matchInfo['hostFinalScore'] = hostFinalScore
        matchInfo['visitingFinalScore'] = visitingFinalScore
        matchInfo['totalScore'] = hostFinalScore + visitingFinalScore
        halfScores = row['half'].split(':')
        hostHalfScore = int(halfScores[0])
        visitingHalfScore = int(halfScores[1])
        matchInfo['hostHalfScore'] = hostHalfScore
        matchInfo['visitingHalfScore'] = visitingHalfScore
        matchInfo['result'] = resultByScore(hostFinalScore, visitingFinalScore)
        matchInfo['letResult'] = resultByScore(hostFinalScore + int(matchInfo['letCount']), visitingFinalScore)
        matchInfo['halfResult'] = resultByScore(hostHalfScore, visitingHalfScore)
        matchInfo['activeOddsLevel'] = getActiveOdds(matchInfo)
      logger.info(matchInfo)
      result[matchId] = matchInfo

  return result

def filter30day(alldata, startTime):
  data = []
  curMiss = dict({
    'low': 0,
    'middle': 0,
    'high': 0,
    'zero': 0,
    'two': 0,
    'four': 0
  })

  for v in alldata.values():
    if v['saleStopTime'] < startTime:
      continue

    if v.get('finalScore'):
      for k in curMiss:
        curMiss[k] += 1
      
      curMiss[v['activeOddsLevel']] = 0
      if v['totalScore'] < 2:
        curMiss['zero'] = 0
      elif v['totalScore'] < 4:
        curMiss['two'] = 0
      elif v['totalScore'] < 6:
        curMiss['four'] = 0
      
      v['miss'] = curMiss.copy()
    data.append(v)
  return data

def calcMiss(data):
  curMiss = dict({
    'low': 0,
    'middle': 0,
    'high': 0,
    'zero': 0,
    'two': 0,
    'four': 0
  })
  maxMiss = dict({
    'low': 0,
    'middle': 0,
    'high': 0,
    'zero': 0,
    'two': 0,
    'four': 0
  })

  for v in data.values():
    if not v.get('finalScore'):
      continue
    for k in curMiss:
      curMiss[k] += 1
    
    curMiss[v['activeOddsLevel']] = 0
    if v['totalScore'] < 2:
      curMiss['zero'] = 0
    elif v['totalScore'] < 4:
      curMiss['two'] = 0
    elif v['totalScore'] < 6:
      curMiss['four'] = 0
    
    for k in curMiss:
      if curMiss[k] > maxMiss[k]:
        maxMiss[k] = curMiss[k]
  
  return maxMiss

def resultByScore(hostScore, visitingScore):
  if hostScore > visitingScore:
    return 1
  elif hostScore == visitingScore:
    return 0
  else:
    return -1

def getActiveOdds(matchInfo):
  odds = matchInfo.get(resultToKey.get(matchInfo['letResult']))
  maxOdds = max(matchInfo['winOdds'], matchInfo['levelOdds'], matchInfo['loseOdds'])
  minOdds = min(matchInfo['winOdds'], matchInfo['levelOdds'], matchInfo['loseOdds'])
  if odds == maxOdds:
    return 'high'
  elif odds == minOdds:
    return 'low'
  else:
    return 'middle'
