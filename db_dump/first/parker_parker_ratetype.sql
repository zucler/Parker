-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: ec2-52-62-202-224.ap-southeast-2.compute.amazonaws.com    Database: parker
-- ------------------------------------------------------
-- Server version	5.5.46

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
-- Table structure for table `parker_ratetype`
--

DROP TABLE IF EXISTS `parker_ratetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parker_ratetype` (
  `rateID` int(11) NOT NULL AUTO_INCREMENT,
  `day_of_week` smallint(6) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `rate_type` varchar(50) NOT NULL,
  `label` varchar(50) NOT NULL,
  `parkingID` int(11) NOT NULL,
  PRIMARY KEY (`rateID`),
  UNIQUE KEY `parker_ratetype_parkingID_6cade2c3_uniq` (`parkingID`,`day_of_week`,`rate_type`,`label`),
  KEY `parker_ratetype_293b48e9` (`parkingID`),
  CONSTRAINT `parker_ratetype_parkingID_c5ec7a06_fk_parker_parking_parkingID` FOREIGN KEY (`parkingID`) REFERENCES `parker_parking` (`parkingID`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parker_ratetype`
--

LOCK TABLES `parker_ratetype` WRITE;
/*!40000 ALTER TABLE `parker_ratetype` DISABLE KEYS */;
INSERT INTO `parker_ratetype` VALUES (1,0,'00:00:00','23:59:00','Hourly','Weekend',1),(2,1,'08:00:00','19:30:00','Flat','Early Bird',1),(3,2,'08:00:00','19:30:00','Flat','Early Bird',1),(4,3,'08:00:00','19:30:00','Flat','Early Bird',1),(5,4,'08:00:00','19:30:00','Flat','Early Bird',1),(6,5,'08:00:00','19:30:00','Flat','Early Bird',1),(7,0,'00:00:00','23:59:00','Hourly','Casual',1),(8,1,'17:00:00','23:59:00','Flat','Night',1),(9,2,'17:00:00','23:59:00','Flat','Night',1),(10,3,'17:00:00','23:59:00','Flat','Night',1),(11,7,'17:00:00','23:59:00','Flat','Night',1),(12,4,'17:00:00','23:59:00','Flat','Night',1),(13,5,'17:00:00','23:59:00','Flat','Night',1),(14,6,'17:00:00','23:59:00','Flat','Night',1),(15,6,'00:00:00','23:59:00','Flat','Weekend',2),(16,7,'00:00:00','23:59:00','Flat','Weekend',2),(17,1,'08:00:00','19:00:00','Flat','Early Bird',2),(18,1,'17:00:00','23:59:00','Flat','Night',2),(19,2,'17:00:00','23:59:00','Flat','Night',2),(20,3,'17:00:00','23:59:00','Flat','Night',2),(21,4,'17:00:00','23:59:00','Flat','Night',2),(22,5,'17:00:00','23:59:00','Flat','Night',2),(23,0,'00:00:00','23:59:00','Hourly','Casual',2),(24,0,'00:00:00','23:59:00','hourly','Casual',5),(25,0,'00:00:00','23:59:00','hourly','Casual',6),(26,0,'00:00:00','23:59:00','hourly','Casual',7),(27,0,'00:00:00','23:59:00','hourly','Weekend',7),(28,1,'16:00:00','04:00:00','flat','Night',7),(29,2,'16:00:00','04:00:00','flat','Night',7),(30,3,'16:00:00','04:00:00','flat','Night',7),(31,1,'06:00:00','19:30:00','flat','Super Early Bird',1),(32,2,'06:00:00','19:30:00','flat','Super Early Bird',1),(33,3,'06:00:00','19:30:00','flat','Super Early Bird',1),(34,4,'06:00:00','19:30:00','flat','Super Early Bird',1),(35,5,'06:00:00','19:30:00','flat','Super Early Bird',1),(36,2,'08:00:00','19:00:00','flat','Early Bird',2),(37,3,'08:00:00','19:00:00','flat','Early Bird',2),(38,4,'08:00:00','19:00:00','flat','Early Bird',2),(39,5,'08:00:00','19:00:00','flat','Early Bird',2),(40,1,'07:00:00','19:00:00','flat','Super Early Bird',2),(41,2,'07:00:00','19:00:00','flat','Super Early Bird',2),(42,3,'07:00:00','19:00:00','flat','Super Early Bird',2),(43,4,'07:00:00','19:00:00','flat','Super Early Bird',2),(44,5,'07:00:00','19:00:00','flat','Super Early Bird',2),(45,1,'06:00:00','19:00:00','flat','Early Bird',3),(46,2,'06:00:00','19:00:00','flat','Early Bird',3),(47,3,'06:00:00','19:00:00','flat','Early Bird',3),(48,4,'06:00:00','19:00:00','flat','Early Bird',3),(49,5,'06:00:00','19:00:00','flat','Early Bird',3),(50,0,'00:00:00','23:59:00','hourly','Casual',3),(51,1,'18:00:00','04:00:00','flat','Night',3),(52,2,'18:00:00','04:00:00','flat','Night',3),(53,3,'18:00:00','04:00:00','flat','Night',3),(54,4,'18:00:00','04:00:00','flat','Night',3),(55,5,'18:00:00','04:00:00','flat','Night',3),(56,6,'18:00:00','04:00:00','flat','Night',3),(57,7,'18:00:00','04:00:00','flat','Night',3),(58,1,'08:00:00','19:00:00','flat','Early Bird',4),(59,2,'08:00:00','19:00:00','flat','Early Bird',4),(60,3,'08:00:00','19:00:00','flat','Early Bird',4),(61,4,'08:00:00','19:00:00','flat','Early Bird',4),(62,5,'08:00:00','19:00:00','flat','Early Bird',4),(63,1,'17:00:00','23:59:00','flat','Night',4),(64,2,'17:00:00','23:59:00','flat','Night',4),(65,3,'17:00:00','23:59:00','flat','Night',4),(66,4,'17:00:00','23:59:00','flat','Night',4),(67,5,'17:00:00','23:59:00','flat','Night',4),(68,6,'00:00:00','23:59:00','flat','Weekend',4),(69,7,'00:00:00','23:59:00','flat','Weekend',4),(70,0,'00:00:00','23:59:00','hourly','Casual',4),(71,1,'07:00:00','19:00:00','flat','Super Early Bird',4),(72,2,'07:00:00','19:00:00','flat','Super Early Bird',4),(73,3,'07:00:00','19:00:00','flat','Super Early Bird',4),(74,4,'07:00:00','19:00:00','flat','Super Early Bird',4),(75,5,'07:00:00','19:00:00','flat','Super Early Bird',4),(76,4,'16:00:00','04:00:00','flat','Night',7),(77,5,'16:00:00','04:00:00','flat','Night',7),(78,6,'16:00:00','04:00:00','flat','Night',7),(79,7,'16:00:00','04:00:00','flat','Night',7),(80,0,'00:00:00','23:59:00','hourly','Casual',8),(81,0,'00:00:00','23:59:00','hourly','Casual',9),(82,6,'00:00:00','23:59:00','flat','Weekend',9),(83,7,'00:00:00','23:59:00','flat','Weekend',9),(84,1,'17:00:00','06:00:00','flat','Night',9),(85,2,'17:00:00','06:00:00','flat','Night',9),(86,3,'17:00:00','06:00:00','flat','Night',9),(87,4,'17:00:00','06:00:00','flat','Night',9),(88,5,'17:00:00','06:00:00','flat','Night',9);
/*!40000 ALTER TABLE `parker_ratetype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-03 11:33:25
