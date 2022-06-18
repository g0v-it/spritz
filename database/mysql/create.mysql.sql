-- MySQL dump 10.13  Distrib 5.7.34, for Win64 (x86_64)
--
-- Host: localhost    Database: spritz
-- ------------------------------------------------------
-- Server version	5.7.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `judgement`
--

DROP TABLE IF EXISTS `judgement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `judgement` (
  `votation_id` int(11) NOT NULL,
  `jud_value` int(11) NOT NULL,
  `jud_name` varchar(50) NOT NULL,
  PRIMARY KEY (`votation_id`,`jud_value`),
  CONSTRAINT `judgement_ibfk_1` FOREIGN KEY (`votation_id`) REFERENCES `votation` (`votation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `judgement`
--

LOCK TABLES `judgement` WRITE;
/*!40000 ALTER TABLE `judgement` DISABLE KEYS */;
/*!40000 ALTER TABLE `judgement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `option`
--

DROP TABLE IF EXISTS `option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `option` (
  `option_id` int(11) NOT NULL AUTO_INCREMENT,
  `votation_id` int(11) DEFAULT NULL,
  `option_name` varchar(50) NOT NULL,
  PRIMARY KEY (`option_id`),
  UNIQUE KEY `votation_id` (`votation_id`,`option_name`),
  CONSTRAINT `option_ibfk_1` FOREIGN KEY (`votation_id`) REFERENCES `votation` (`votation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `option`
--

LOCK TABLES `option` WRITE;
/*!40000 ALTER TABLE `option` DISABLE KEYS */;
/*!40000 ALTER TABLE `option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votation`
--

DROP TABLE IF EXISTS `votation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `votation` (
  `votation_id` int(11) NOT NULL AUTO_INCREMENT,
  `promoter_user_id` int(11) DEFAULT NULL,
  `votation_description` varchar(500) NOT NULL,
  `description_url` varchar(500) NOT NULL,
  `begin_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `votation_type` varchar(10) NOT NULL,
  `votation_status` int(11) NOT NULL,
  `list_voters` int(11) NOT NULL,
  PRIMARY KEY (`votation_id`),
  UNIQUE KEY `votation_description` (`votation_description`),
  KEY `promoter_user_id` (`promoter_user_id`),
  CONSTRAINT `votation_ibfk_1` FOREIGN KEY (`promoter_user_id`) REFERENCES `votinguser` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votation`
--

LOCK TABLES `votation` WRITE;
/*!40000 ALTER TABLE `votation` DISABLE KEYS */;
/*!40000 ALTER TABLE `votation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote` (
  `vote_key` varchar(128) NOT NULL,
  `votation_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL,
  `jud_value` int(11) NOT NULL,
  PRIMARY KEY (`vote_key`,`votation_id`,`option_id`),
  KEY `votation_id` (`votation_id`),
  KEY `option_id` (`option_id`),
  CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`votation_id`) REFERENCES `votation` (`votation_id`),
  CONSTRAINT `vote_ibfk_2` FOREIGN KEY (`option_id`) REFERENCES `option` (`option_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voter`
--

DROP TABLE IF EXISTS `voter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voter` (
  `user_id` int(11) NOT NULL,
  `votation_id` int(11) NOT NULL,
  `voted` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`votation_id`),
  KEY `votation_id` (`votation_id`),
  CONSTRAINT `voter_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `votinguser` (`user_id`),
  CONSTRAINT `voter_ibfk_2` FOREIGN KEY (`votation_id`) REFERENCES `votation` (`votation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voter`
--

LOCK TABLES `voter` WRITE;
/*!40000 ALTER TABLE `voter` DISABLE KEYS */;
/*!40000 ALTER TABLE `voter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votinguser`
--

DROP TABLE IF EXISTS `votinguser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `votinguser` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(200) NOT NULL,
  `pass_word` varchar(200) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `verified` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votinguser`
--

LOCK TABLES `votinguser` WRITE;
/*!40000 ALTER TABLE `votinguser` DISABLE KEYS */;
INSERT INTO `votinguser` VALUES (1,'aldo','aldo',NULL,NULL),(2,'beppe','beppe',NULL,NULL),(3,'carlo','carlo',NULL,NULL),(4,'dario','dario',NULL,NULL),(5,'ernesto','ernesto',NULL,NULL),(6,'fabio','fabio',NULL,NULL);
/*!40000 ALTER TABLE `votinguser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-18 21:10:13
