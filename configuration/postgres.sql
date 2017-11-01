-- PostgreSQL script for configuration table
-- (tested with PostgreSQL 10.0, should work with 8.x and later)

﻿-- DROP ENTITIES:
  -- Constraint: agency_job_configuration_agency_description_uq
  -- Constraint: agency_job_configuration_export_url_uq
  -- Constraint: agency_job_configuration_pk
  -- Table: agency_job_configuration

ALTER TABLE IF EXISTS agency_job_configuration
    DROP CONSTRAINT agency_job_configuration_agency_description_uq;

ALTER TABLE IF EXISTS agency_job_configuration
    DROP CONSTRAINT agency_job_configuration_export_url_uq;

ALTER TABLE IF EXISTS agency_job_configuration
    DROP CONSTRAINT agency_job_configuration_pk;

DROP TABLE IF EXISTS agency_job_configuration;

﻿-- CREATE ENTITIES:
  -- Table: agency_job_configuration
  -- Constraint: agency_job_configuration_pk
  -- Constraint: agency_job_configuration_export_url_uq
  -- Constraint: agency_job_configuration_uq

CREATE TABLE agency_job_configuration
(
    id_agency_job_configuration serial NOT NULL,
    agency_description character varying(255) NOT NULL,
    agency_homepage character varying(255),
    export_url character varying(255) NOT NULL,
    opt_i18n boolean NOT NULL DEFAULT false,
    opt_video boolean NOT NULL DEFAULT false,
    opt_virtual boolean NOT NULL DEFAULT false,
    opt_latlng boolean NOT NULL DEFAULT false,
    opt_geo_id boolean NOT NULL DEFAULT false,
    opt_flag_storico boolean NOT NULL DEFAULT false,
    opt_note_nascoste boolean NOT NULL DEFAULT false,
    opt_abstract boolean NOT NULL DEFAULT false,
    opt_finiture boolean NOT NULL DEFAULT false,
    opt_micro_categorie boolean NOT NULL DEFAULT false,
    opt_stima boolean NOT NULL DEFAULT false,
    opt_ind_reale boolean NOT NULL DEFAULT false,
    opt_agente boolean NOT NULL DEFAULT false,
    opt_persone boolean NOT NULL DEFAULT false,
    image_resize boolean NOT NULL DEFAULT true,
    image_normalize boolean NOT NULL DEFAULT true,
    image_apply_watermark boolean NOT NULL DEFAULT false,
)
WITH (
    OIDS = FALSE
);

ALTER TABLE agency_job_configuration
    ADD CONSTRAINT agency_job_configuration_pk PRIMARY KEY (id_agency_job_configuration);

ALTER TABLE agency_job_configuration
    ADD CONSTRAINT agency_job_configuration_export_url_uq UNIQUE (export_url);

ALTER TABLE agency_job_configuration
    ADD CONSTRAINT agency_job_configuration_agency_description_uq UNIQUE (agency_description);

