import enum


@enum.unique
class DatoDisponibile(enum.Enum):

    fatturato = 1
    fee_di_ingresso = 2
    volumetria = 3
    mq_giardino = 4
    mq_aree_esterne = 5
    altezza_piano = 6
    kw_cabina_elettrica = 7
    distanza_dal_mare = 8
    numero_chiavi = 17
    mq_ufficio = 18
    superficie_lotto = 19
    superficie_commerciale = 20
    superficie_utile = 21
    dimensione_accesso_carraio = 22
    lunghezza = 23
    larghezza = 24
    altezza = 25
    potenza_impianto_elettrico = 26
    deposito_cauzionale = 27
    fideiussione = 28
