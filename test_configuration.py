import unittest
import os
import inspect

from peewee import Database

import configuration
from configuration.db_access import db_proxy, JobGlobalOption, AgencySyncConfiguration


def mock_result() -> configuration.LocalConfiguration:
    return configuration.LocalConfiguration(dict(
        gi_homepage='http://gi.com/',
        connection_timeout=10,
        agencies=[
            dict(
                rome=None,
                description="Rome agency",
                homepage="http://www.domain.com/",
                export_url="https://pannello.gestionaleimmobiliare.it/export_xml_annunci1.html",
                options=dict(
                    i18n=False,
                    video=False,
                    virtual=False,
                    latlng=False,
                    geo_id=False,
                    flag_storico=False,
                    note_nascoste=False,
                    abstract=False,
                    finiture=False,
                    micro_categorie=False,
                    stima=False,
                    ind_reale=False,
                    agente=False,
                    persone=False),
                image=dict(
                    resize=True,
                    normalize=True,
                    apply_watermark=False
                )
            ),
            dict(
                milan=None,
                description="Milan agency",
                homepage="http://www.domain2.com/",
                export_url="https://pannello.gestionaleimmobiliare.it/export_xml_annunci2.html",
                options=dict(
                    i18n=False,
                    video=False,
                    virtual=False,
                    latlng=False,
                    geo_id=True,
                    flag_storico=False,
                    note_nascoste=False,
                    abstract=False,
                    finiture=False,
                    micro_categorie=False,
                    stima=True,
                    ind_reale=False,
                    agente=False,
                    persone=False),
                image=dict(
                    resize=True,
                    normalize=True,
                    apply_watermark=False
                )
            )
        ]
    ))


class DBSettingsSerializationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['GISYNC_CONFIGURATION'] = '{                               ' \
                                             '    "conf_type": "mysql",       ' \
                                             '    "connection_args": {        ' \
                                             '         "host": "localhost",   ' \
                                             '         "port": 3306,          ' \
                                             '         "user": "nice_boat",   ' \
                                             '         "password": "password",' \
                                             '         "database": "test_db"  ' \
                                             '   }                            ' \
                                             '}                               '

    @classmethod
    def tearDownClass(cls):
        del os.environ['GISYNC_CONFIGURATION']

    def test_deserialize_db_settings(self):

        # small hack for good. Getting private member function of module in order to test it
        get_db_settings = inspect.getmembers(
            configuration,
            lambda f: inspect.isfunction(f) and f.__name__ == '__get_settings_configuration'
        )[0][1]

        self.assertDictEqual(get_db_settings(), {'conf_type': 'mysql',
                                                 'connection_args': {
                                                     'user': 'nice_boat',
                                                     'password': 'password',
                                                     'database': 'test_db',
                                                     'port': 3306,
                                                     'host': 'localhost'
                                                    }
                                                 })


class DBConfigurationTests(unittest.TestCase):

    @staticmethod
    def mock_data_generation(database: Database):

        AgencySyncConfiguration._meta.schema = ''
        JobGlobalOption._meta.schema = ''

        database.create_tables([JobGlobalOption, AgencySyncConfiguration])

        JobGlobalOption.create(option_name='gi_sync_agenzia.gi_homepage',
                               option_value='http://gi.com/')
        JobGlobalOption.create(option_name='gi_sync_agenzia.connection_timeout',
                               option_value='10')

        AgencySyncConfiguration.create(agency_description="Rome agency",
                                       agency_homepage="http://www.domain.com/",
                                       export_url='https://pannello.gestionaleimmobiliare.it/export_xml_annunci1.html')
        AgencySyncConfiguration.create(agency_description="Milan agency",
                                       agency_homepage="http://www.domain2.com/",
                                       export_url='https://pannello.gestionaleimmobiliare.it/export_xml_annunci2.html',
                                       opt_geo_id=True, opt_stima=True)

    @classmethod
    def setUpClass(cls):
        os.environ['GISYNC_CONFIGURATION'] = '{"conf_type":"unittest", "connection_args": {}}'
        db_proxy.attach_callback(DBConfigurationTests.mock_data_generation)

    @classmethod
    def tearDownClass(cls):
        del os.environ['GISYNC_CONFIGURATION']

    def test_query(self):
        self.assertEqual(configuration.get(), mock_result())


class YamlFileConfigurationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['GISYNC_CONFIGURATION'] = '{"conf_type":"yaml", "file": {"location": "config.yaml"}}'

    @classmethod
    def tearDownClass(cls):
        del os.environ['GISYNC_CONFIGURATION']

    def test_get_configuration(self):
        self.assertEqual(configuration.get(), mock_result())
