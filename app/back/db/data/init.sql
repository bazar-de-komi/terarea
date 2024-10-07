/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.8-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: terarea
-- ------------------------------------------------------
-- Server version	11.5.2-MariaDB-ubu2404

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `terarea`
--

CREATE DATABASE IF NOT EXISTS `terarea` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;

USE `terarea`;

--
-- Table structure for table `Actions`
--

DROP TABLE IF EXISTS `Actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actions` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(400) NOT NULL DEFAULT 'zero two, darling, darling... DARLING !!!',
  `trigger` mediumtext NOT NULL DEFAULT 'Elle est où la pierre ?',
  `consequences` mediumtext NOT NULL DEFAULT 'DANS LA POCHE !!!',
  `author` bigint(20) unsigned NOT NULL,
  `tags` longtext DEFAULT NULL COMMENT '''The tags used to find the the actions the user created.''',
  `running` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'L''information sur si le l''action est en fonctionnement',
  `description` varchar(2000) NOT NULL DEFAULT 'Some description' COMMENT 'The description of the workflow.',
  `colour` varchar(100) NOT NULL DEFAULT '#f1f1f1' COMMENT 'The colour of the workflow.',
  `favicon` varchar(900) DEFAULT NULL COMMENT 'The link to the icon of the workflow.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `Actions_UNIQUE` (`name`),
  KEY `Actions_Users_FK` (`author`),
  CONSTRAINT `Actions_Users_FK` FOREIGN KEY (`author`) REFERENCES `Users` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='triggers and actions of ifttt\nexample: if bad_guy then nuts';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Actions`
--

LOCK TABLES `Actions` WRITE;
/*!40000 ALTER TABLE `Actions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Connections`
--

DROP TABLE IF EXISTS `Connections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Connections` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `token` varchar(900) DEFAULT NULL COMMENT 'The token of the user.',
  `usr_id` bigint(20) unsigned DEFAULT NULL COMMENT 'The e-mail of the user.',
  `expiration_date` datetime DEFAULT NULL COMMENT 'The date at which the token is invalidated.',
  PRIMARY KEY (`id`),
  KEY `Connections_Users_FK` (`usr_id`),
  CONSTRAINT `Connections_Users_FK` FOREIGN KEY (`usr_id`) REFERENCES `Users` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='The active connections of the server.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Connections`
--

LOCK TABLES `Connections` WRITE;
/*!40000 ALTER TABLE `Connections` DISABLE KEYS */;
/*!40000 ALTER TABLE `Connections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Services`
--

DROP TABLE IF EXISTS `Services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Services` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `url` varchar(2048) NOT NULL,
  `key` varchar(1024) NOT NULL COMMENT 'api token',
  `Categorie` varchar(200) NOT NULL COMMENT 'This is the type of service offered by the api',
  `frequency` bigint(20) unsigned NOT NULL DEFAULT 0 COMMENT '''The amount of tymes the service is used''',
  `type` varchar(200) NOT NULL DEFAULT 'service' COMMENT 'The type of the api.',
  `tags` longtext DEFAULT NULL COMMENT 'The keywords to search for the api',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `Services_UNIQUE_1` (`name`),
  UNIQUE KEY `Services_UNIQUE` (`url`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='api info';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Services`
--

LOCK TABLES `Services` WRITE;
/*!40000 ALTER TABLE `Services` DISABLE KEYS */;
/*!40000 ALTER TABLE `Services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserServices`
--

DROP TABLE IF EXISTS `UserServices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserServices` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `service_id` bigint(20) unsigned NOT NULL,
  `area_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `UserServices_Users_FK` (`user_id`),
  KEY `UserServices_Services_FK` (`service_id`),
  KEY `UserServices_Actions_FK` (`area_id`),
  CONSTRAINT `UserServices_Actions_FK` FOREIGN KEY (`area_id`) REFERENCES `Actions` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `UserServices_Services_FK` FOREIGN KEY (`service_id`) REFERENCES `Services` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `UserServices_Users_FK` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='services user subscribed to';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserServices`
--

LOCK TABLES `UserServices` WRITE;
/*!40000 ALTER TABLE `UserServices` DISABLE KEYS */;
/*!40000 ALTER TABLE `UserServices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `email` varchar(320) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `method` varchar(200) DEFAULT NULL,
  `favicon` varchar(900) DEFAULT NULL COMMENT 'The link to the icon of the user account.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `Users_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Verification`
--

DROP TABLE IF EXISTS `Verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Verification` (
  `id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `key` mediumtext DEFAULT NULL COMMENT 'This is the identification for the code reference.',
  `code` mediumtext NOT NULL,
  `expiration` datetime DEFAULT NULL COMMENT 'The time meft before the code expires.',
  PRIMARY KEY (`id`),
  UNIQUE KEY `Verification_UNIQUE` (`code`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='This is the table in charge of storing the verification codes for user side events.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Verification`
--

LOCK TABLES `Verification` WRITE;
/*!40000 ALTER TABLE `Verification` DISABLE KEYS */;
/*!40000 ALTER TABLE `Verification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-07 16:36:14
