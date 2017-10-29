from io import BytesIO
from datetime import datetime
from typing import Union, Optional
from lxml import objectify
from lxml import etree

from .mapping.info_inserite import InfoInserita
from .mapping.dati_disponibili import DatoDisponibile


SYNC_AGENZIA_FAKE_NS = 'http://gestionaleimmobiliare.it/export/sync_agenzia'


class SyncAgenziaAgent:

    def __init__(self):
        pass

    @staticmethod
    def synchronize_wordpress():
        print('start sync')


class SyncInterpreter:

    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    @staticmethod
    def enrich_xml(xml_string: str) -> str:

        doc = objectify.parse(BytesIO(bytearray(xml_string, 'UTF-8')))
        dataset = doc.getroot()
        dataset.set('xmlns', SYNC_AGENZIA_FAKE_NS)

        for info_tag in dataset.xpath('//dataset/annuncio/info'):
            info_tag.set('id', str(info_tag.id))

        return etree.tostring(doc)

    @staticmethod
    def build_parser() -> etree.XMLParser:

        parser = objectify.makeparser(remove_blank_text=True)
        lookup = etree.ElementNamespaceClassLookup(fallback=objectify.ObjectifyElementClassLookup())
        parser.set_element_class_lookup(lookup)

        namespace = lookup.get_namespace(SYNC_AGENZIA_FAKE_NS)

        for element in (ApeElement, AllegatoElement, IncaricoElement,
                        InfoElement, DatoDisponibileElement, InfoInseriteElement, DatiDisponibiliElement):
            namespace[element.tag_name] = element

        return parser

    @staticmethod
    def parse_xml(xml_string: str) -> etree.ElementTree:

        objectify.PyType('date', DateElement.check_date, DateElement).register()

        doc = objectify.parse(BytesIO(SyncInterpreter.enrich_xml(xml_string)),
                              parser=SyncInterpreter.build_parser())

        return doc


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


class InfoElement(objectify.ObjectifiedElement):

    tag_name = 'info'

    @property
    def id(self) -> Optional[int]:
        try:
            return int(self.get('id'))
        except TypeError:
            return None

    @property
    def information_type(self) -> Optional[InfoInserita]:
        try:
            return InfoInserita(self.id)
        except ValueError:
            return None

    @property
    def mapped_value(self) -> Union[InfoInserita, int, bool, None]:
        try:
            return self.information_type.mapped_value(self.valore_assegnato)
        except ValueError:
            return None

    @property
    def keep_in_list(self) -> Optional[bool]:
        try:
            return self.information_type.keep_in_list(self.valore_assegnato)
        except ValueError:
            return None


class InfoInseriteElement(objectify.ObjectifiedElement):

    tag_name = 'info_inserite'

    def by_information_type(self, info_inserita: InfoInserita) -> Optional[InfoElement]:
        for info in self.iterchildren():
            if info.id == info_inserita.value:
                return info


class DatoDisponibileElement(objectify.IntElement):

    tag_name = 'dati'

    @property
    def id(self) -> int:
        return int(self.get('id'))

    @property
    def information_type(self) -> DatoDisponibile:
        return DatoDisponibile(self.id)


class DatiDisponibiliElement(objectify.ObjectifiedElement):

    tag_name = 'dati_inseriti'

    def by_information_type(self, dato_disponibile: DatoDisponibile) -> Optional[DatoDisponibileElement]:
        for dato in self.iterchildren():
            if dato.id == dato_disponibile.value:
                return dato
