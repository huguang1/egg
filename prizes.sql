-- MySQL dump 10.13  Distrib 5.5.57, for Linux (x86_64)
--
-- Host: localhost    Database: egg
-- ------------------------------------------------------
-- Server version	5.5.57-log

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
-- Table structure for table `lottery_prize`
--

DROP TABLE IF EXISTS `lottery_prize`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lottery_prize` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prize_id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `desc` varchar(250) NOT NULL,
  `probability` decimal(8,3) DEFAULT NULL,
  `is_show` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lottery_prize`
--

LOCK TABLES `lottery_prize` WRITE;
/*!40000 ALTER TABLE `lottery_prize` DISABLE KEYS */;
INSERT INTO `lottery_prize` VALUES (1,1,'9元现金筹码','9元现金筹码',40.000,1),(2,2,'15元现金筹码','15元现金筹码',8.000,1),(3,3,'18元现金筹码','18元现金筹码',5.000,1),(4,4,'28元现金筹码','28元现金筹码',1.000,1),(5,5,'38元现金筹码','38元现金筹码',0.500,1),(6,6,'58元现金筹码','58元现金筹码',0.200,1),(7,7,'88元现金筹码','88元现金筹码',0.100,1),(8,8,'188元现金筹码','188元现金筹码',0.080,1),(9,9,'288元现金筹码','288元现金筹码',0.050,1),(10,10,'388元现金筹码','388元现金筹码',0.020,1),(11,11,'谢谢参与','谢谢参与',30.000,1);
/*!40000 ALTER TABLE `lottery_prize` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-08 19:31:58
