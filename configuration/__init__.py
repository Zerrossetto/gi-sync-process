import json
import os
import yaml

from collections import OrderedDict
from typing import List, Union, Optional
from threading import RLock

from .db_access import db_initialize, JobGlobalOption, AgencySyncConfiguration


class ImageProcessingConfiguration:

    def __init__(self, processing_opts: dict):
        self.processing_opts = processing_opts

    @property
    def resize(self) -> bool:
        return self.processing_opts.get('resize', True)

    @property
    def normalize(self) -> bool:
        return self.processing_opts.get('normalize', True)

    @property
    def apply_watermark(self) -> bool:
        return self.processing_opts.get('apply_watermark', False)

    def __eq__(self, other):

        if other is self:
            return True
        elif other is None or type(other) is not ImageProcessingConfiguration:
            return False

        return self.processing_opts == other.processing_opts

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<configuration.ImageProcessingConfiguration opts={}>'.format(self.processing_opts)


class AgencyConfiguration:

    def __init__(self, conf: Union[dict, AgencySyncConfiguration]):

        conf_type = type(conf)

        if conf_type == dict:
            self.__set_internals(conf['description'],
                                 conf['export_url'],
                                 conf.get('homepage'),
                                 {k: bool(v) for k, v in conf['options'].items()},
                                 {k: bool(v) for k, v in conf['image'].items()})

        elif conf_type == AgencySyncConfiguration:
            self.__set_internals(conf.agency_description,
                                 conf.export_url,
                                 conf.agency_homepage,
                                 conf.options_dictionary,
                                 conf.image_processing_dictionary)
        else:
            raise AttributeError('Invalid collection type: {}'.format(conf_type.__name__))

    def __set_internals(self,
                        description: str,
                        export_url: str,
                        homepage: str,
                        sync_options: dict,
                        image_processing: dict):
        self.description = description
        self.export_url = export_url
        self.homepage = homepage
        self.sync_options = OrderedDict(sorted(sync_options.items(), key=lambda t: t[0]))
        self.image_processing = ImageProcessingConfiguration(image_processing)

    def __eq__(self, other):

        if other is self:
            return True
        elif other is None or type(other) is not AgencyConfiguration:
            return False

        return self.description == other.description \
            and self.export_url == other.export_url \
            and self.homepage == other.homepage \
            and self.sync_options == other.sync_options \
            and self.image_processing == other.image_processing

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<configuration.AgencyConfig decr="{o.description}" ' \
               'export_url={o.export_url} opts={o.sync_options} ' \
               'image={o.image_processing}>'.format(o=self)


class LocalConfiguration:

    DEFAULT_TIMEOUT = 30

    def __init__(self, base_config: dict, agencies_config: List[AgencySyncConfiguration] = None):

        self.base_config = base_config

        if agencies_config is None:
            if 'agencies' not in base_config or len(base_config['agencies']) == 0:
                self.agencies_conf = []
            else:
                self.agencies_conf = list([AgencyConfiguration(ac) for ac in base_config['agencies']])
                del self.base_config['agencies']
        else:
            if len(agencies_config) == 0:
                self.agencies_conf = []
            else:
                self.agencies_conf = [AgencyConfiguration(ac) for ac in agencies_config]

    @property
    def gi_homepage(self) -> Optional[str]:
        return self.base_config.get('gi_homepage')

    @property
    def connection_timeout(self) -> int:
        try:
            return int(self.base_config['connection_timeout'])
        except (KeyError, TypeError):  # conf value not found or value not valid
            return self.DEFAULT_TIMEOUT

    @property
    def agencies_configuration(self) -> List[AgencyConfiguration]:
        return self.agencies_conf

    def __eq__(self, other):

        if other is self:
            return True
        elif other is None or type(other) is not LocalConfiguration:
            return False

        return self.gi_homepage == other.gi_homepage \
            and self.connection_timeout == other.connection_timeout \
            and self.agencies_conf == other.agencies_conf

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<configuration.LocalConfiguration ' \
               'hp={hp} timeout={timeout}, ' \
               'agencies_configuration={agencies}>'.format(hp=self.gi_homepage,
                                                           timeout=self.connection_timeout,
                                                           agencies=self.agencies_conf)


__conf_instance = None


def __get_settings_configuration():
    return json.loads(os.getenv('GISYNC_CONFIGURATION'))


def get() -> LocalConfiguration:

    global __conf_instance

    with RLock():  # defend __conf_instance from duplicate db access
        if __conf_instance is None:

            settings = __get_settings_configuration()
            conf_type = settings['conf_type']

            if conf_type == 'yaml':

                with open(settings['file']['location']) as config_file:
                    __conf_instance = LocalConfiguration(yaml.load(config_file)['base_config'])

            elif conf_type in db_access.handled_db_types():

                db = db_initialize(settings)
                prefix = 'gi_sync_agenzia.'
                __conf_instance = LocalConfiguration(
                    {opt.option_name[len(prefix):]: opt.option_value for opt in db_access.global_options(prefix)},
                    db_access.agencies_options()
                )
                db.close()

    return __conf_instance
