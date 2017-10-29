import enum
from typing import Any


@enum.unique
class Tag(enum.Enum):

    room = 1
    sell_type = 2
    furniture = 3
    location = 4


@enum.unique
class EnergyLabel(enum.Enum):

    da_definire = 0
    A_plus_passiva = 1
    A = 2
    B = 3
    C = 4
    D = 5
    E = 6
    F = 7
    G = 8
    non_soggetto_certificazione = 9
    A4 = 10
    A3 = 11
    A2 = 12
    A1 = 13

    @property
    def is_ape_2015(self):
        return self.value > 9

    @staticmethod
    def keep_in_list(value) -> bool:
        return True


@enum.unique
class Location(enum.Enum):

    sconosciuta = 0
    area_industriale_artigianale = 1
    centro_commerciale = 2
    ad_angolo = 3
    centrale = 4
    servita = 5
    forte_passaggio = 6
    fronte_lago = 7
    fronte_strada = 8
    interna = 9

    @staticmethod
    def keep_in_list(value) -> bool:
        return True


@enum.unique
class ManteinanceLevel(enum.Enum):

    sconosciuto = 0
    da_ristrutturare = 1
    ristrutturato = 2
    discreto = 3
    buono = 4
    ottimo = 5
    nuovo = 6
    impianti_da_fare = 7
    impianti_da_rifare = 8
    impianti_a_norma = 9

    @staticmethod
    def keep_in_list(value) -> bool:
        return bool(value)


@enum.unique
class Panorama(enum.Enum):

    non_indicato = 0
    vista_mare = 1
    vista_lago = 2
    vista_monti = 3
    vista_aperta = 4
    vista_monumento = 5
    vista_giardino = 6
    fronte_mare = 7
    lato_mare = 8

    @staticmethod
    def keep_in_list(value) -> bool:
        return bool(value)

@enum.unique
class Sign(enum.Enum):

    no = 0
    si = 1
    rimosso = 2
    da_rimuovere = 3

    @staticmethod
    def keep_in_list(value) -> bool:
        return True


@enum.unique
class Awnings(enum.Enum):

    no = 0
    si = 1
    predisposto = 2

    @staticmethod
    def keep_in_list(value) -> bool:
        return bool(value)


@enum.unique
class ElectricalSystem(enum.Enum):

    non_definito = 0
    da_fare = 1
    a_norma = 2
    da_verificare = 3

    @staticmethod
    def keep_in_list(value) -> bool:
        return bool(value)


@enum.unique
class Connectivity(enum.Enum):

    nessuna = 0
    adsl = 1
    fibra = 2

    @staticmethod
    def keep_in_list(value) -> bool:
        return True


repr_format = '<{0:}.{1:}: {2:d}, type={3:} tags={4:}>'

@enum.unique
class InfoInserita(enum.Enum):

    bagni = (Tag.room,)
    camere = (Tag.room,)
    cucina = (Tag.room,), bool
    soggiorno = (Tag.room,), bool
    garage = (Tag.room,), bool
    asta = (), bool
    ripostigli = ()
    cantina = (Tag.room,), bool
    vendita = (Tag.sell_type,), bool
    affitto = (Tag.sell_type,), bool
    mansarda = (Tag.room,), bool
    tavena = (), bool
    ascensore = (), bool
    aria_condizionata = (), bool
    arredo = (), bool
    riscaldamento_autonomo = (), bool
    giardino = (), bool
    ingresso_indipendente = (), bool
    garage_doppio = (), bool
    posto_auto = (), bool
    riscaldamento_a_pavimento = (), bool
    soggiorno_con_angolo_cottura = (), bool
    allarme = (), bool
    terrazzi = ()
    poggioli = ()
    lavanderia = (), bool
    piano_interrato = (), bool
    piano_terra = (), bool
    primo_piano = (), bool
    piano_intermedio = (), bool
    ultimo_piano = (), bool
    totale_piani = ()
    piano_numero = ()
    riscaldamento_centralizzato = (), bool
    mare = (Tag.location,), bool
    montagna = (Tag.location,), bool
    lago = (Tag.location,), bool
    terme = (Tag.location,), bool
    collina = (Tag.location,), bool
    campagna = (Tag.location,), bool
    nuovo = (), bool
    immobile_di_prestigio = (), bool
    giardino_condominiale = (), bool
    soffitta = (), bool
    grezzo = (), bool
    camino = (), bool
    predisposizione_aria_condizionata = (), bool
    predisposizione_allarme = (), bool
    pannelli_solari = (), bool
    pannelli_fotovoltaici = (), bool
    impianto_geotermico = (), bool
    aree_esterne = (), bool
    ribalte = (), bool
    urbanizzato = (), bool
    classe_energetica = (), EnergyLabel
    posizione = (), Location
    stato_manutenzione = (), ManteinanceLevel
    numero_vetrine = ()
    carro_ponte = (), bool
    impianto_anti_incendio = (), bool
    cabina_elettrica = (), bool
    panorama = (), Panorama
    piano_semi_interrato = (), bool
    piano_rialzato = (), bool
    numero_locali = (), bool
    piscina = (), bool
    porticato = (), bool
    soppalco = (), bool
    sottotetto = (), bool
    chiavi_in_agenzia = (), bool
    accesso_disabili = (), bool
    area_fitness = (), bool
    frigorifero = (Tag.furniture,), bool
    lavatrice = (Tag.furniture,), bool
    lavastoviglie = (Tag.furniture,), bool
    posto_spiaggia = (), bool
    cassaforte = (Tag.furniture,), bool
    animali_ammessi = (), bool
    televisore = (Tag.furniture,), bool
    forno = (Tag.furniture,), bool
    vasca_idromassaggio = (Tag.furniture,), bool
    caldaia_a_condensazione = (), bool
    riscaldamento_semi_autonomo = (), bool
    riscaldamento_termopompa = (), bool
    raffreddamento = (), bool
    cucina_arredata = (), bool
    portineria = (), bool
    domotica = (), bool
    tapparelle_motorizzate = (), bool
    porta_blindata = (), bool
    contacalorie = (), bool
    montacarichi = ()
    banchine_di_carico = ()
    numero_portoni = ()
    numero_accessi_carrai = ()
    cartello = (), Sign
    saracinesche = ()
    vasca = (Tag.furniture,), bool
    zanzariere = (), bool
    tende_da_sole = (Tag.furniture,), Awnings
    impianto_elettrico = ()
    allacciamento_fognatura = (), bool
    canna_fumaria = (), bool
    connettivita = ()
    impianto_illuminazione = (), bool

    def __new__(cls, *args):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__) + 1
        return obj

    def __init__(self, *args):
        try:
            self.tags = args[0]
        except IndexError:
            self.tags = ()
        try:
            self.value_type = args[1]
        except IndexError:
            self.value_type = int

    @property
    def is_enum(self) -> bool:
        return issubclass(self.value_type, enum.Enum)

    def keep_in_list(self, value) -> bool:
        if self.is_enum:
            return self.value_type.keep_in_list(value)
        else:
            return bool(value)

    def mapped_value(self, reference_value: int) -> Any:
        return self.value_type(reference_value)

    def __repr__(self):
        return self.name

    def __str__(self):
        return repr_format.format(self.__class__.__name__,
                                  self.name,
                                  self.value,
                                  self.value_type.__name__,
                                  self.tags)
