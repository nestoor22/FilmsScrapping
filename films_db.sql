-- MySQL Script generated by MySQL Workbench
-- Sun Oct 27 11:25:55 2019
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema films_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema films_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `films_db` DEFAULT CHARACTER SET utf8 ;
USE `films_db` ;

-- -----------------------------------------------------
-- Table `films_db`.`films`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `films_db`.`films` (
  `film_id` INT NOT NULL AUTO_INCREMENT,
  `name_rus` VARCHAR(100) NOT NULL,
  `name_eng` VARCHAR(45) NOT NULL,
  `imdb_rating` FLOAT NULL DEFAULT NULL,
  `release_date` INT NOT NULL,
  `plot` LONGTEXT NOT NULL,
  `poster_url` varchar(500) NULL DEFAULT NULL,
  PRIMARY KEY (`film_id`),
  INDEX `Name_Index` (`name_rus` ASC, `name_eng` ASC) VISIBLE,
  INDEX `Year` (`release_date` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `films_db`.`actors`
-- -----------------------------------------------------
CREATE TABLE `actors` (
  `actor_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `number_of_films` int(11) DEFAULT NULL,
  PRIMARY KEY (`actor_id`),
  KEY `Actor_Name` (`name`))
ENGINE=InnoDB;


-- -----------------------------------------------------
-- Table `films_db`.`genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `films_db`.`genres` (
  `genre_id` INT NOT NULL AUTO_INCREMENT,
  `genre_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`genre_id`),
  INDEX `genre_name` (`genre_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `films_db`.`film_genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `films_db`.`film_genre` (
  `film_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`film_id`, `genre_id`),
  INDEX `fk_film_genre_genres1_idx` (`genre_id` ASC) VISIBLE,
  CONSTRAINT `fk_film_genre_films`
    FOREIGN KEY (`film_id`)
    REFERENCES `films_db`.`films` (`film_id`)
    ON DELETE cascade
    ON UPDATE cascade,
  CONSTRAINT `fk_film_genre_genres1`
    FOREIGN KEY (`genre_id`)
    REFERENCES `films_db`.`genres` (`genre_id`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `films_db`.`film_actors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `films_db`.`film_actors` (
  `film_id` INT NOT NULL,
  `actor_id` INT NOT NULL,
  PRIMARY KEY (`film_id`, `actor_id`),
  CONSTRAINT `fk_film_actors_films1`
    FOREIGN KEY (`film_id`)
    REFERENCES `films_db`.`films` (`film_id`)
    ON DELETE cascade
    ON UPDATE cascade,
  CONSTRAINT `fk_film_actors_actors1`
    FOREIGN KEY (`film_id`)
    REFERENCES `films_db`.`actors` (`actor_id`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `films_db`.`countries`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `films_db`.`countries` (
  `country_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`name`),
  INDEX `Country_Name` (`country_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `films_db`.`film_country`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `films_db`.`film_country` (
  `film_id` INT NOT NULL,
  `country_id` INT NOT NULL,
  PRIMARY KEY (`film_id`, `country_id`),
  INDEX `fk_film_country_countries1_idx` (`country_id` ASC) VISIBLE,
  CONSTRAINT `fk_film_country_films1`
    FOREIGN KEY (`film_id`)
    REFERENCES `films_db`.`films` (`film_id`)
    ON DELETE cascade
    ON UPDATE cascade,
  CONSTRAINT `fk_film_country_countries1`
    FOREIGN KEY (`country_id`)
    REFERENCES `films_db`.`countries` (`country_id`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
