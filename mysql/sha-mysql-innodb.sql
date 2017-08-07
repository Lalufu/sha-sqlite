DROP TABLE IF EXISTS `sha`;
CREATE TABLE `sha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sha` varbinary(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

