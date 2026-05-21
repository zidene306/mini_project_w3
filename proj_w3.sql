
CREATE DATABASE proj_w3;
USE proj_w3;
CREATE TABLE IF NOT EXISTS `location_table` (
	`country_id` BIGINT NOT NULL,
	`country_name` VARCHAR(255) NOT NULL,
	`continent` VARCHAR(255) NOT NULL,
	PRIMARY KEY(`country_id`)
);


CREATE TABLE IF NOT EXISTS `year_table` (
	`year_id` BIGINT NOT NULL,
	`year` INTEGER NOT NULL,
	PRIMARY KEY(`year_id`)
);


CREATE TABLE IF NOT EXISTS `energy_statistics` (
	`stat_id` BIGINT NOT NULL,
	`country_id` BIGINT NOT NULL,
	`year_id` BIGINT NOT NULL,
	`renewables_share_energy` DECIMAL NOT NULL,
	`fossil_share_energy` DECIMAL NOT NULL,
	`renewables_share_elec` DECIMAL NOT NULL,
	PRIMARY KEY(`stat_id`)
);


CREATE TABLE IF NOT EXISTS `population` (
	`pop_id` BIGINT NOT NULL,
	`gdp` BIGINT NOT NULL,
	`country_id` BIGINT NOT NULL,
	`year_id` BIGINT NOT NULL,
	PRIMARY KEY(`pop_id`)
);


ALTER TABLE `energy_statistics`
ADD FOREIGN KEY(`country_id`) REFERENCES `location_table`(`country_id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `energy_statistics`
ADD FOREIGN KEY(`year_id`) REFERENCES `year_table`(`year_id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `population`
ADD FOREIGN KEY(`country_id`) REFERENCES `location_table`(`country_id`)
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE `population`
ADD FOREIGN KEY(`year_id`) REFERENCES `year_table`(`year_id`)
ON UPDATE CASCADE ON DELETE CASCADE;
