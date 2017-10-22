from io import BytesIO, StringIO
from datetime import datetime
from lxml import objectify
from lxml import etree


SYNC_AGENZIA_FAKE_NS = 'http://gestionaleimmobiliare.it/export/sync_agenzia'


class SyncAgenziaAgent:

    def __init__(self):
        pass

    def synchronize_wordpress(self):
        print('start sync')


class SyncInterpreter:

    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    @staticmethod
    def parse_xml(xml_string: str) -> etree.ElementTree:
        doc = objectify.parse(BytesIO(bytearray(xml_string, 'UTF-8')))
        doc.getroot().set('xmlns', SYNC_AGENZIA_FAKE_NS)

        objectify.PyType('date', DateElement.check_date, DateElement).register()

        parser = objectify.makeparser(remove_blank_text=True)
        lookup = etree.ElementNamespaceClassLookup(fallback=objectify.ObjectifyElementClassLookup())
        parser.set_element_class_lookup(lookup)

        namespace = lookup.get_namespace(SYNC_AGENZIA_FAKE_NS)

        for element in (ApeElement, AllegatoElement, IncaricoElement):
            namespace[element.tag_name] = element

        return objectify.parse(BytesIO(etree.tostring(doc)), parser=parser)


class DateElement(objectify.ObjectifiedDataElement):

    date_format = '%Y-%m-%d %H:%M:%S'

    @property
    def pyval(self):
        return datetime.strptime(self.text, DateElement.date_format)

    @staticmethod
    def check_date(string_date):
        datetime.strptime(string_date, DateElement.date_format)


class ApeElement(objectify.StringElement):

    tag_name = 'ape'

    @property
    def version(self):
        return int(self.get('version'))

    @property
    def epgl_ren(self):
        return float(self.get('epgl_ren'))

    @property
    def epgl_nren(self):
        return float(self.get('epgl_nren'))

    @property
    def flag_quasi_zero(self):
        return bool(int(self.get('flag_quasi_zero')))

    @property
    def prestazione_estate(self):
        return self.get('prestazione_estate')

    @property
    def prestazione_inverno(self):
        return self.get('prestazione_inverno')

class AllegatoElement(objectify.ObjectifiedElement):

    tag_name = 'allegato'

    @property
    def planimetria(self):
        return self.is_blueprint()

    def is_blueprint(self):
        return bool(int(self.get('planimetria')))

class IncaricoElement(objectify.StringElement):

    tag_name = 'incarico'

    @property
    def inizio(self):
        return self.get('inizio')

    @property
    def fine(self):
        return self.get('fine')