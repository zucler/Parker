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
-- Table structure for table `parker_parking`
--

DROP TABLE IF EXISTS `parker_parking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parker_parking` (
  `parkingID` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(500) NOT NULL,
  `address` longtext NOT NULL,
  `lat` decimal(10,6) NOT NULL,
  `long` decimal(10,6) NOT NULL,
  `parking_type` varchar(150) NOT NULL,
  `places_of_interest` longtext NOT NULL,
  `uri` longtext NOT NULL,
  PRIMARY KEY (`parkingID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parker_parking`
--

LOCK TABLES `parker_parking` WRITE;
/*!40000 ALTER TABLE `parker_parking` DISABLE KEYS */;
INSERT INTO `parker_parking` VALUES (1,'Queen Victoria Building Car Park','111 York Street, Sydney',-33.871109,151.206243,'Wilson','(Entertainment) STATE THEATRE\r\n(Family) Sydney Tower Eye\r\n(Shopping) Pitt st Mall','http://wilsonparking.com.au/park/2036_Queen-Victoria-Building-Car-Park_111-York-Street-Sydney'),(2,'St Martins Tower Car Park','190-202 Clarence Street, Sydney',-33.871420,151.203594,'Wilson','(Entertainment) State Theatre\r\n(Landmarks) Cockle Bay Wharf\r\n(Public Institutions) Sydney Town Hall','https://www.wilsonparking.com.au/park/2135_St-Martins-Tower-Car-Park_190-202-Clarence-Street-Sydney'),(3,'Harbourside Car Park','100 Murray Street, Pyrmont',-33.871290,151.195385,'Wilson','Harbourside Shopping Centre, Darling Harbour, IMAX, Madame Tussauds Sydney, Wild Life Sydney Zoo, The Star','https://www.wilsonparking.com.au/park/2047_Harbourside-Car-Park_100-Murray-Street-Pyrmont'),(4,'175 Liverpool St Car Park','26 Nithsdale Street, Sydney\n26 Nithsdale Street, Sydney\n26 Nithsdale Street, Sydney\n26 Nithsdale Street, Sydney',-33.877853,151.208100,'Wilson','(Entertainment) Capitol Theatre','https://www.wilsonparking.com.au/park/2024_175-Liverpool-St-Car-Park_26-Nithsdale-Street-Sydney'),(5,'East Village Car Park','4 Defries Avenue, Zetland',-33.905890,151.210313,'Wilson','','https://www.wilsonparking.com.au/park/2260_East-Village-Car-Park_4-Defries-Avenue-Zetland'),(6,'Macquarie Shopping Centre Car Park','Cnr Herring & Waterloo Roads, North Ryde',-33.776880,151.118162,'Wilson','','https://www.wilsonparking.com.au/park/2219_Macquarie-Shopping-Centre-Car-Park_Cnr-Herring--Waterloo-Roads-North-Ryde-'),(7,'169-179 Thomas Street Car Park','169-179 Thomas Street Car Park',-33.881828,151.200540,'Wilson','(Entertainment) Quantas Credit Arena, (Entertainment) Capitoal Theatre, (Education & Museums)\nPOWERHOUSE MUSEUM','https://www.wilsonparking.com.au/park/2108_169-179-Thomas-Street-Car-Park_169-179-Thomas-Street-Haymarket'),(8,'Sydney Airport International Car Park','Sydney International Airport Station, Mascot',-33.939923,151.173088,'Wilson','','https://www.wilsonparking.com.au/park/2099_Sydney-Airport-International-Car-Park_Sydney-International-Airport-Station-Mascot'),(9,'Eagle Street Pier Car Park','45 Eagle Street, Brisbane',-27.468988,153.028419,'Wilson','','https://www.wilsonparking.com.au/park/4062_Eagle-Street-Pier-Car-Park_45-Eagle-Street-Brisbane'),(10,'425 Collins Street','425 Collins Street',-37.817492,144.958452,'Wilson','','https://www.wilsonparking.com.au/park/3296_425-Collins-Street_425-Collins-Street');
/*!40000 ALTER TABLE `parker_parking` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-03 11:32:48
