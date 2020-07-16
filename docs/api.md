# API文档

## 足球赛事列表

### 请求：
```
GET /match/getFootball
```
### 参数
无

### 返回
```
[
  {
    "matchId": 125542,                // 赛事ID
    "league": "英冠",                 // 联赛名称
    "hostTeam": "利兹联",             // 主队名称
    "visitingTeam": "巴恩斯利",       // 客队名称
    "matchPeriod": "2020-07-16",      // 赛事周期（售卖周期）
    "number": "周四001",              // 赛事编号
    "saleStopTime": 1594915200000,    // 开赛时间
    "isSpf": "Selling",               // 胜平负售卖状态（Selling 为售卖中）
    "isSingle": "0",                  // 胜平负是否单关
    "win": "1.20",                    // 胜 赔率
    "level": "5.05",                  // 平 赔率
    "lose": "9.70",                   // 负 赔率
    "isRqspf": "Selling",             // 让球胜平负售卖状态
    "isLetSingle": "0",               // 让球胜平负是否单关
    "letCount": "-1",                 // 让球数
    "letWin": "1.72",                 // 让胜 赔率
    "letLevel": "3.70",               // 让平 赔率
    "letLose": "3.48",                // 让负 赔率
    "isBf": "Selling",                // 总比分售卖状态
    "zeroToZero": "16.00",            // 0:0 赔率
    "zeroToOne": "22.00",             // 0:1 赔率
    "zeroToTwo": "50.00",             // 0:2 赔率
    "zeroToThree": "120.0",           // 0:3 赔率
    "zeroToFour": "400.0",            // 0:4 赔率
    "zeroToFive": "1000",             // 0:5 赔率
    "oneToZero": "6.40",              // 1:0 赔率
    "oneToOne": "8.25",               // 1:1 赔率
    "oneToTwo": "19.00",              // 1:2 赔率
    "oneToThree": "70.00",            // 1:3 赔率
    "oneToFour": "250.0",             // 1:4 赔率
    "oneToFive": "800.0",             // 1:5 赔率
    "twoToZero": "5.90",              // 2:0 赔率
    "twoToOne": "7.00",               // 2:1 赔率
    "twoToTwo": "19.00",              // 2:2 赔率
    "twoToThree": "60.00",            // 2:3 赔率
    "twoToFour": "250.0",             // 2:4 赔率
    "twoToFive": "800.0",             // 2:5 赔率
    "threeToZero": "7.50",            // 3:0 赔率
    "threeToOne": "10.00",            // 3:1 赔率
    "threeToTwo": "22.00",            // 3:2 赔率
    "threeToThree": "80.00",          // 3:3 赔率
    "fourToZero": "13.00",            // 4:0 赔率
    "fourToOne": "19.00",             // 4:1 赔率
    "fourToTwo": "35.00",             // 4:2 赔率
    "fiveToZero": "25.00",            // 5:0 赔率
    "fiveToOne": "35.00",             // 5:1 赔率
    "fiveToTwo": "80.00",             // 5:2 赔率
    "winOther": "22.00",              // 胜其他 赔率
    "levelOther": "400.0",            // 平其他 赔率
    "loseOther": "250.0",             // 负其他 赔率
    "isBqc": "Selling",               // 半全场售卖状态
    "winWin": "1.73",                 // 胜-胜 赔率
    "winLevel": "22.00",              // 胜-平 赔率
    "winLose": "60.00",               // 胜-负 赔率
    "levelWin": "3.75",               // 平-胜 赔率
    "levelLevel": "7.00",             // 平-平 赔率
    "levelLose": "18.00",             // 平-负 赔率
    "loseWin": "25.00",               // 负-胜 赔率
    "loseLevel": "22.00",             // 负-平 赔率
    "loseLose": "16.00",              // 负-负 赔率
    "isZjq": "Selling",               // 总进球数售卖状态
    "zero": "16.00",                  // 0球 赔率
    "one": "5.70",                    // 1球 赔率
    "two": "3.75",                    // 2球 赔率
    "three": "3.35",                  // 3球 赔率
    "four": "4.55",                   // 4球 赔率
    "five": "8.00",                   // 5球 赔率
    "six": "16.00",                   // 6球 赔率
    "seven": "24.00"                  // 7+球 赔率
  },...
]
```

## 奖金计算

### 请求：

```
POST /result/calcBonus
```

### 参数：
```
{
  "betting": [                         // 投注信息
    {
      "matchNumber":"周四001",         // 赛事编号
      "bettingItems":["win", "seven"]  // 投注项，可选值参见投注项列表
    },
    {
      "matchNumber":"周四002",
      "bettingItems":["winWin"]
    }
  ],
  "options": ["single", "2x1"],        // 玩法
  "multiple": 1,                       // 倍数
  "bettingTime": 1594910200000         // 投注时间
}
```

### 返回
```
{
  "status": 0,                         // 状态码，值为 0 时表示成功，失败情况参见状态码列表
  "bonus": "102.4",                    // 计算得出的奖金
}
```

### 投注项列表
| key | 含义 |
| --- | --- |
| win | 胜 |
| level | 平 |
| lose | 负|
| letWin | 让胜 |
| letLevel | 让平 |
| letLose | 让负 |
| zeroToZero | 0:0 |
| zeroToOne | 0:1 |
| zeroToTwo | 0:2 |
| zeroToThree | 0:3 |
| zeroToFour | 0:4 |
| zeroToFive | 0:5 |
| oneToZero | 1:0 |
| oneToOne | 1:1 |
| oneToTwo | 1:2 |
| oneToThree | 1:3 |
| oneToFour | 1:4 |
| oneToFive | 1:5 |
| twoToZero | 2:0 |
| twoToOne | 2:1 |
| twoToTwo | 2:2 |
| twoToThree | 2:3 |
| twoToFour | 2:4 |
| twoToFive | 2:5 |
| threeToZero | 3:0 |
| threeToOne | 3:1 |
| threeToTwo | 3:2 |
| threeToThree | 3:3 |
| fourToZero | 4:0 |
| fourToOne | 4:1 |
| fourToTwo | 4:2 |
| fiveToZero | 5:0 |
| fiveToOne | 5:1 |
| fiveToTwo | 5:2 |
| winOther | 胜其他 |
| levelOther | 平其他 |
| loseOther | 负其他 |
| winWin | 胜-胜 |
| winLevel | 胜-平 |
| winLose | 胜-负 |
| levelWin | 平-胜 |
| levelLevel | 平-平 |
| levelLose | 平-负 |
| loseWin | 负-胜 |
| loseLevel | 负-平 |
| loseLose | 负-负 |
| zero | 0球 |
| one | 1球 |
| two | 2球 |
| three | 3球 |
| four | 4球 |
| five | 5球 |
| six | 6球 |
| seven | 7+球 |

### 状态码对照表
| status | 含义 |
| --- | --- |
| 0 | 成功 |
| 100 | 有赛事未出结果 |

## 赛果时间预测

### 请求：

```
POST /result/predictTime
```

### 参数：
```
{
  "matchNumber": "周四001"           // 赛事编号
}
```

### 返回
```
{
  "status": 0,                       // 状态码，值为 0 时表示成功，失败情况参见状态码列表
  "resultTime": 1594910200000        // 预计可以出结果的时间
}
```

### 状态码对照表
| status | 含义 |
| --- | --- |
| 0 | 成功 |
| 404 | 赛事不存在 |
