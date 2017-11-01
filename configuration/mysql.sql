-- MySQL script for configuration table
-- (tested with MySQL 5.7.20, don't know older ones)

﻿-- DROP ENTITIES:
  -- Table: job_configuration

DROP TABLE `agency_sync_configuration`;

﻿-- CREATE ENTITIES:
  -- Table: job_configuration

CREATE TABLE `agency_sync_configuration` (
  `id_agency_job_configuration` INTEGER NOT NULL AUTO_INCREMENT,
  `agency_description` VARCHAR(255) NOT NULL,
  `agency_homepage` VARCHAR(255) NULL,
  `export_url` VARCHAR(255) NOT NULL,
  `opt_i18n` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_video` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_virtual` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_latlng` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_geo_id` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_flag_storico` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_note_nascoste` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_abstract` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_finiture` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_micro_categorie` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_stima` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_ind_reale` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_agente` BOOLEAN NOT NULL DEFAULT FALSE,
  `opt_persone` BOOLEAN NOT NULL DEFAULT FALSE,
  `image_resize` BOOLEAN NOT NULL DEFAULT TRUE,
  `image_normalize` BOOLEAN NOT NULL DEFAULT TRUE,
  `image_apply_watermark` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY `job_configuration` (`id_agency_job_configuration`),
  UNIQUE INDEX `agency_description_uq` (`agency_description` ASC));
  UNIQUE INDEX `export_url_uq` (`export_url` ASC));
