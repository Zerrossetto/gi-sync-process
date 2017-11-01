import inspect
import os
import peewee

from typing import List

db_proxy = peewee.Proxy()


class BaseDBConfiguration(peewee.Model):

    class Meta:
        database = db_proxy
        schema = os.getenv('GISYNC_SCHEMA', 'gi_sync_agenzia')


class JobGlobalOption(BaseDBConfiguration):

    class Meta:
        db_table = os.getenv('GISYNC_JOB_CONF_TABLE', 'wp_options')

    option_id = peewee.PrimaryKeyField()
    option_name = peewee.CharField(max_length=64, null=False, unique=True)
    option_value = peewee.TextField(null=False)
    autoload = peewee.CharField(max_length=20, default='yes', null=False)


class AgencySyncConfiguration(BaseDBConfiguration):

    class Meta:
        db_table = os.getenv('GISYNC_AGENCY_CONF_TABLE', 'agency_sync_configuration')

    string_format = '<db_access.JobConfiguration: {o.id_job_configuration:d} agency="{o.agency_description}", ' \
                    'options: i18n={o.opt_i18n:d} video={o.opt_video:d} virtual={o.opt_virtual:d} ' \
                    'latlng={o.opt_latlng:d} geo_id={o.opt_geo_id:d} flag_storico={o.opt_flag_storico:d} ' \
                    'note_nascoste={o.opt_note_nascoste:d} abstract={o.opt_abstract:d} finiture={o.opt_finiture:d} ' \
                    'micro_categorie={o.opt_micro_categorie:d} stima={o.opt_stima:d} ind_reale={o.opt_ind_reale:d} ' \
                    'agente={o.opt_agente:d} persone={o.opt_persone:d}>'

    id_job_configuration = peewee.PrimaryKeyField()

    agency_description = peewee.CharField(unique=True, max_length=255, null=False)
    agency_homepage = peewee.CharField(unique=True, max_length=255, null=True)
    export_url = peewee.CharField(unique=True, max_length=255, null=False)

    # sync options
    opt_i18n = peewee.BooleanField(default=False, null=False)
    opt_video = peewee.BooleanField(default=False, null=False)
    opt_virtual = peewee.BooleanField(default=False, null=False)
    opt_latlng = peewee.BooleanField(default=False, null=False)
    opt_geo_id = peewee.BooleanField(default=False, null=False)
    opt_flag_storico = peewee.BooleanField(default=False, null=False)
    opt_note_nascoste = peewee.BooleanField(default=False, null=False)
    opt_abstract = peewee.BooleanField(default=False, null=False)
    opt_finiture = peewee.BooleanField(default=False, null=False)
    opt_micro_categorie = peewee.BooleanField(default=False, null=False)
    opt_stima = peewee.BooleanField(default=False, null=False)
    opt_ind_reale = peewee.BooleanField(default=False, null=False)
    opt_agente = peewee.BooleanField(default=False, null=False)
    opt_persone = peewee.BooleanField(default=False, null=False)

    # image processing options
    image_resize = peewee.BooleanField(default=True, null=False)
    image_normalize = peewee.BooleanField(default=True, null=False)
    image_apply_watermark = peewee.BooleanField(default=False, null=False)

    def __str__(self):
        return AgencySyncConfiguration.string_format.format(o=self)

    @property
    def options_dictionary(self) -> dict:
        return self.__subfields_to_dict('opt_')

    @property
    def image_processing_dictionary(self) -> dict:
        return self.__subfields_to_dict('image_')

    def __subfields_to_dict(self, prefix: str) -> dict:
        """
        Returns key-value of instance fields whose key starts with a given prefix

        :param prefix: the prefix to filter the result with
        :return: a kv dictionary
        """
        opt_fields = inspect.getmembers( AgencySyncConfiguration, lambda m: issubclass(type(m), peewee.Field))
        return {key[len(prefix):]: getattr(self, key) for key, value in opt_fields if key.startswith(prefix)}


def __get_postgres_connection(db_type: str, **kwargs) -> peewee.Database:
    return peewee.PostgresqlDatabase(**kwargs)


def __get_mysql_connection(db_type: str, **kwargs) -> peewee.Database:
    return peewee.MySQLDatabase(**kwargs)


def __get_sqlite_inmemory_connection(db_type: str, **kwargs) -> peewee.Database:
    return peewee.SqliteDatabase(':memory:')


def __invalid_db_type(db_type: str, **kwargs) -> None:
    raise AttributeError('Invalid db type {}'.format(db_type))

__db_internal_factory = {
    'postgres': __get_postgres_connection,
    'mysql': __get_mysql_connection,
    'sqlite_inmemory': __get_sqlite_inmemory_connection,
    'unittest': __get_sqlite_inmemory_connection
}


def handled_db_types() -> List[str]:
    return [k for k, v in __db_internal_factory.items()]


def db_initialize(settings: dict) -> peewee.Database:

    factory = __db_internal_factory.get(settings['conf_type'], __invalid_db_type)
    database = factory(settings['conf_type'], **settings['connection_args'])
    db_proxy.initialize(database)

    return database


def global_options() -> peewee._ModelQueryResultWrapper:
    return JobGlobalOption.select().where(JobGlobalOption.option_name ** 'gi_sync_agenzia.%').execute()


def agencies_options() -> peewee._ModelQueryResultWrapper:
    return AgencySyncConfiguration.select().execute()
