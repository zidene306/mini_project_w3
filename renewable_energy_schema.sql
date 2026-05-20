CREATE DATABASE renewable_energy;

USE renewable_energy;

CREATE TABLE IF NOT EXISTS `fact_energy` (
	`fact_id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
	`entity_id` INTEGER UNSIGNED,
	`year_id` INTEGER UNSIGNED,
	`indicator_id` INTEGER UNSIGNED,
	`value` DOUBLE,
	PRIMARY KEY(`fact_id`)
);


CREATE TABLE IF NOT EXISTS `entity` (
	`entity_id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
	`iso_code` VARCHAR(255),
	`entity_name` VARCHAR(255),
	`entity_type` VARCHAR(255),
	PRIMARY KEY(`entity_id`)
);


CREATE TABLE IF NOT EXISTS `year` (
	`year_id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
	`year` INTEGER,
	`decade` VARCHAR(255),
	PRIMARY KEY(`year_id`)
);


CREATE TABLE IF NOT EXISTS `indicator` (
	`indicator_id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE,
	`indicator_name` VARCHAR(255),
	`category` VARCHAR(255),
	`unit` VARCHAR(255),
	PRIMARY KEY(`indicator_id`)
);


ALTER TABLE `fact_energy`
ADD FOREIGN KEY(`entity_id`) REFERENCES `entity`(`entity_id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `fact_energy`
ADD FOREIGN KEY(`year_id`) REFERENCES `year`(`year_id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `fact_energy`
ADD FOREIGN KEY(`indicator_id`) REFERENCES `indicator`(`indicator_id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;