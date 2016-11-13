-- MySQL dump 10.13  Distrib 5.7.16, for Linux (x86_64)
--
-- Host: parker-db    Database: parker
-- ------------------------------------------------------
-- Server version	5.7.16

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
-- Current Database: `parker`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `parker` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `parker`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add user',2,'add_user'),(5,'Can change user',2,'change_user'),(6,'Can delete user',2,'delete_user'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add group',4,'add_group'),(11,'Can change group',4,'change_group'),(12,'Can delete group',4,'delete_group'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add parking',7,'add_parking'),(20,'Can change parking',7,'change_parking'),(21,'Can delete parking',7,'delete_parking'),(22,'Can add rate type',8,'add_ratetype'),(23,'Can change rate type',8,'change_ratetype'),(24,'Can delete rate type',8,'delete_ratetype'),(25,'Can add rate price',9,'add_rateprice'),(26,'Can change rate price',9,'change_rateprice'),(27,'Can delete rate price',9,'delete_rateprice'),(28,'Can add dependency',10,'add_dependency'),(29,'Can change dependency',10,'change_dependency'),(30,'Can delete dependency',10,'delete_dependency');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$30000$HCLcq8aZjc68$LHiLi12+gTS+DazPX20OmSSEef5dabryQayyeE99ozM=','2016-11-13 06:44:45.102432',1,'root','','','',1,1,'2016-11-13 06:44:33.814060');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(4,'auth','group'),(3,'auth','permission'),(2,'auth','user'),(5,'contenttypes','contenttype'),(7,'parker','parking'),(9,'parker','rateprice'),(8,'parker','ratetype'),(6,'sessions','session'),(10,'static_precompiler','dependency');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-11-13 06:42:41.355858'),(2,'auth','0001_initial','2016-11-13 06:42:41.504749'),(3,'admin','0001_initial','2016-11-13 06:42:41.546265'),(4,'admin','0002_logentry_remove_auto_add','2016-11-13 06:42:41.558514'),(5,'contenttypes','0002_remove_content_type_name','2016-11-13 06:42:41.602093'),(6,'auth','0002_alter_permission_name_max_length','2016-11-13 06:42:41.613964'),(7,'auth','0003_alter_user_email_max_length','2016-11-13 06:42:41.626268'),(8,'auth','0004_alter_user_username_opts','2016-11-13 06:42:41.635502'),(9,'auth','0005_alter_user_last_login_null','2016-11-13 06:42:41.656419'),(10,'auth','0006_require_contenttypes_0002','2016-11-13 06:42:41.658883'),(11,'auth','0007_alter_validators_add_error_messages','2016-11-13 06:42:41.668775'),(12,'auth','0008_alter_user_username_max_length','2016-11-13 06:42:41.683783'),(13,'sessions','0001_initial','2016-11-13 06:42:41.698314'),(14,'static_precompiler','0001_initial','2016-11-13 06:42:41.721511'),(15,'parker','0001_initial','2016-11-13 06:47:30.123804');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('u6zejmp9r62writhcjyjdl769a9t2a1y','OTJkOTQ1MWZjMzViNzI3ZmEyYmY3NzUyYTI3MTA1NDgyMTA1OTU5MTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMGU4ZWNmYjdiMzY3MGRjZjQyOWFkMDNkNGRlNjliODEzMmY2MDQ2OSIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-11-27 06:44:45.105477');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `parker_rateprice`
--

DROP TABLE IF EXISTS `parker_rateprice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parker_rateprice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `duration` int(11) NOT NULL,
  `price` decimal(10,6) NOT NULL,
  `rateID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `parker_rateprice_duration_fd9d8f15_uniq` (`duration`,`rateID`),
  KEY `parker_rateprice_0be6f211` (`rateID`),
  CONSTRAINT `parker_rateprice_rateID_e1b1f4e7_fk_parker_ratetype_rateID` FOREIGN KEY (`rateID`) REFERENCES `parker_ratetype` (`rateID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parker_rateprice`
--

LOCK TABLES `parker_rateprice` WRITE;
/*!40000 ALTER TABLE `parker_rateprice` DISABLE KEYS */;
/*!40000 ALTER TABLE `parker_rateprice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parker_ratetype`
--

DROP TABLE IF EXISTS `parker_ratetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parker_ratetype` (
  `rateID` int(11) NOT NULL AUTO_INCREMENT,
  `day_of_week` smallint(6) NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `rate_type` varchar(50) NOT NULL,
  `label` varchar(50) NOT NULL,
  `parkingID` int(11) NOT NULL,
  PRIMARY KEY (`rateID`),
  UNIQUE KEY `parker_ratetype_parkingID_6cade2c3_uniq` (`parkingID`,`day_of_week`,`rate_type`,`label`),
  CONSTRAINT `parker_ratetype_parkingID_c5ec7a06_fk_parker_parking_parkingID` FOREIGN KEY (`parkingID`) REFERENCES `parker_parking` (`parkingID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parker_ratetype`
--

LOCK TABLES `parker_ratetype` WRITE;
/*!40000 ALTER TABLE `parker_ratetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `parker_ratetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `static_precompiler_dependency`
--

DROP TABLE IF EXISTS `static_precompiler_dependency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `static_precompiler_dependency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(255) NOT NULL,
  `depends_on` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `static_precompiler_dependency_source_d8e91940_uniq` (`source`,`depends_on`),
  KEY `static_precompiler_dependency_36cd38f4` (`source`),
  KEY `static_precompiler_dependency_1f903a40` (`depends_on`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `static_precompiler_dependency`
--

LOCK TABLES `static_precompiler_dependency` WRITE;
/*!40000 ALTER TABLE `static_precompiler_dependency` DISABLE KEYS */;
/*!40000 ALTER TABLE `static_precompiler_dependency` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-13  6:50:59
