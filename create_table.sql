DROP TABLE IF EXISTS matchinfo; CREATE TABLE matchinfo (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL UNIQUE,
    `league` varchar(20),
    `leagueAbbr` varchar(5),
    `leagueId` int,
    `hostTeam` varchar(20),
    `hostTeamAbbr` varchar(5),
    `hostTeamId` int,
    `hostTeamOrder` varchar(10),
    `visitingTeam` varchar(20),
    `visitingTeamAbbr` varchar(5),
    `visitingTeamId` int,
    `visitingTeamOrder` varchar(10),
    `matchPeriod` date,
    `number` varchar(10),
    `printStopTime` bigint,
    `saleStopTime` bigint,
    `startTime` bigint,
    `stopTime` bigint,
    `matchStatus` varchar(10),
    `half` varchar(5),
    `final` varchar(5),
    `500fid` int,
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset utf8mb4;

DROP TABLE IF EXISTS spf; CREATE TABLE spf (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL UNIQUE,
    `isSpf` varchar(10),
    `isSingle` varchar(5),
    `win` varchar(5),
    `level` varchar(5),
    `lose` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset utf8mb4;
      
DROP TABLE IF EXISTS rqspf; CREATE TABLE rqspf (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL UNIQUE,
    `isRqspf` varchar(10),
    `isLetSingle` varchar(5),
    `letCount` varchar(5),
    `letWin` varchar(5),
    `letLevel` varchar(5),
    `letLose` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset utf8mb4;

DROP TABLE IF EXISTS bf; CREATE TABLE bf (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL UNIQUE,
    `isBf` varchar(10),
    `zeroToZero` varchar(5),
    `zeroToOne` varchar(5),
    `zeroToTwo` varchar(5),
    `zeroToThree` varchar(5),
    `zeroToFour` varchar(5),
    `zeroToFive` varchar(5),
    `oneToZero` varchar(5),
    `oneToOne` varchar(5),
    `oneToTwo` varchar(5),
    `oneToThree` varchar(5),
    `oneToFour` varchar(5),
    `oneToFive` varchar(5),
    `twoToZero` varchar(5),
    `twoToOne` varchar(5),
    `twoToTwo` varchar(5),
    `twoToThree` varchar(5),
    `twoToFour` varchar(5),
    `twoToFive` varchar(5),
    `threeToZero` varchar(5),
    `threeToOne` varchar(5),
    `threeToTwo` varchar(5),
    `threeToThree` varchar(5),
    `fourToZero` varchar(5),
    `fourToOne` varchar(5),
    `fourToTwo` varchar(5),
    `fiveToZero` varchar(5),
    `fiveToOne` varchar(5),
    `fiveToTwo` varchar(5),
    `winOther` varchar(5),
    `levelOther` varchar(5),
    `loseOther` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset utf8mb4;

DROP TABLE IF EXISTS bqc; CREATE TABLE bqc (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL UNIQUE,
    `isBqc` varchar(10),
    `winWin` varchar(5),
    `winLevel` varchar(5),
    `winLose` varchar(5),
    `levelWin` varchar(5),
    `levelLevel` varchar(5),
    `levelLose` varchar(5),
    `loseWin` varchar(5),
    `loseLevel` varchar(5),
    `loseLose` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset utf8mb4;

DROP TABLE IF EXISTS zjq; CREATE TABLE zjq (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL UNIQUE,
    `isZjq` varchar(10),
    `zero` varchar(5),
    `one` varchar(5),
    `two` varchar(5),
    `three` varchar(5),
    `four` varchar(5),
    `five` varchar(5),
    `six` varchar(5),
    `seven` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset utf8mb4;

DROP TABLE IF EXISTS spfodds; CREATE TABLE spfodds (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL,
    `isSingle` varchar(5),
    `win` varchar(5),
    `level` varchar(5),
    `lose` varchar(5),
    `releaseTime` bigint,
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uniq_matchId_releaseTime` (`matchId`, `releaseTime`)
) default charset utf8mb4;
      
DROP TABLE IF EXISTS rqspfodds; CREATE TABLE rqspfodds (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL,
    `releaseTime` bigint,
    `isLetSingle` varchar(5),
    `letCount` varchar(5),
    `letWin` varchar(5),
    `letLevel` varchar(5),
    `letLose` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uniq_matchId_releaseTime` (`matchId`, `releaseTime`)
) default charset utf8mb4;

DROP TABLE IF EXISTS bfodds; CREATE TABLE bfodds (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL,
    `releaseTime` bigint,
    `zeroToZero` varchar(5),
    `zeroToOne` varchar(5),
    `zeroToTwo` varchar(5),
    `zeroToThree` varchar(5),
    `zeroToFour` varchar(5),
    `zeroToFive` varchar(5),
    `oneToZero` varchar(5),
    `oneToOne` varchar(5),
    `oneToTwo` varchar(5),
    `oneToThree` varchar(5),
    `oneToFour` varchar(5),
    `oneToFive` varchar(5),
    `twoToZero` varchar(5),
    `twoToOne` varchar(5),
    `twoToTwo` varchar(5),
    `twoToThree` varchar(5),
    `twoToFour` varchar(5),
    `twoToFive` varchar(5),
    `threeToZero` varchar(5),
    `threeToOne` varchar(5),
    `threeToTwo` varchar(5),
    `threeToThree` varchar(5),
    `fourToZero` varchar(5),
    `fourToOne` varchar(5),
    `fourToTwo` varchar(5),
    `fiveToZero` varchar(5),
    `fiveToOne` varchar(5),
    `fiveToTwo` varchar(5),
    `winOther` varchar(5),
    `levelOther` varchar(5),
    `loseOther` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uniq_matchId_releaseTime` (`matchId`, `releaseTime`)
) default charset utf8mb4;

DROP TABLE IF EXISTS bqcodds; CREATE TABLE bqcodds (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL,
    `releaseTime` bigint,
    `winWin` varchar(5),
    `winLevel` varchar(5),
    `winLose` varchar(5),
    `levelWin` varchar(5),
    `levelLevel` varchar(5),
    `levelLose` varchar(5),
    `loseWin` varchar(5),
    `loseLevel` varchar(5),
    `loseLose` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uniq_matchId_releaseTime` (`matchId`, `releaseTime`)
) default charset utf8mb4;

DROP TABLE IF EXISTS zjqodds; CREATE TABLE zjqodds (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL,
    `releaseTime` bigint,
    `zero` varchar(5),
    `one` varchar(5),
    `two` varchar(5),
    `three` varchar(5),
    `four` varchar(5),
    `five` varchar(5),
    `six` varchar(5),
    `seven` varchar(5),
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uniq_matchId_releaseTime` (`matchId`, `releaseTime`)
) default charset utf8mb4;

DROP TABLE IF EXISTS matchstatus; CREATE TABLE matchstatus (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `matchId` int NOT NULL,
    `matchStatus` varchar(10),
    `hostFinalScore` int,
    `visitingFinalScore` int,
    `hostHalfScore` int,
    `visitingHalfScore` int,
    `result` text,
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uniq_matchId` (`matchId`)
) default charset utf8mb4;

DROP TABLE IF EXISTS saletime; CREATE TABLE saletime (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `date` date NOT NULL UNIQUE,
    `startTime` bigint NOT NULL,
    `stopTime` bigint NOT NULL,
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY `idx_date` (`date`)
) default charset utf8mb4;

DROP TABLE IF EXISTS crawlerlog; CREATE TABLE crawlerlog (
    `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `date` date NOT NULL,
    `type` varchar(50),
    `sha256` char(64) NOT NULL,
    `content` mediumtext NOT NULL,
    `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY `idx_date_sha256` (`date`, `sha256`)
) default charset utf8mb4;
