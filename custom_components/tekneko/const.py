DOMAIN = "tekneko"
CONF_CITY_ID = "city_id"
CONF_ZONE_ID = "zone_id"

BASE_API_URL = "https://backoffice.innovambiente.it/wsserver/services"
BIN_SHARED_KEY = "BraininAppInnovambiente"

DEFAULT_CITY_ID = 1341
DEFAULT_ZONE_ID = 1

SUPPORTED_CITIES = {
    1341: "Vetralla",
}

UPDATE_INTERVAL_MINUTES = 60

WASTE_TYPE_MAP = {
    1: "Compostaggio Domestico",
    2: "Rifiuti Ingombranti",
    3: "Plastica",
    4: "Carta",
    5: "Carta e Cartone",
    6: "Vetro",
    7: "Metalli",
    8: "Rifiuti Pericolosi",
    9: "Indifferenziato",
    10: "Plastica e Metalli",
    11: "Organico",
    12: "Sfalci e Potature",
    13: "Olio Vegetale Esausto",
    14: "Abiti e Indumenti Usati",
    15: "Pannolini e Pannoloni",
    16: "Multimateriale",
}

WASTE_ICONS = {
    1: "mdi:leaf",
    2: "mdi:truck",
    3: "mdi:recycle",
    4: "mdi:newspaper",
    5: "mdi:package-variant",
    6: "mdi:glass-fragile",
    7: "mdi:nail",
    8: "mdi:biohazard",
    9: "mdi:trash-can",
    10: "mdi:recycle",
    11: "mdi:fruit-cherries",
    12: "mdi:tree",
    13: "mdi:oil",
    14: "mdi:tshirt-crew",
    15: "mdi:baby",
    16: "mdi:recycle",
}

WASTE_NAMES_IT = {
    1: "Compostaggio Domestico",
    2: "Rifiuti Ingombranti",
    3: "Plastica",
    4: "Carta",
    5: "Carta e Cartone",
    6: "Vetro",
    7: "Metalli",
    8: "Rifiuti Pericolosi",
    9: "Indifferenziato",
    10: "Plastica e Metalli",
    11: "Organico",
    12: "Sfalci e Potature",
    13: "Olio Vegetale Esausto",
    14: "Abiti e Indumenti Usati",
    15: "Pannolini e Pannoloni",
    16: "Multimateriale",
}

WASTE_TYPES_TO_CODE = {
    "Compostaggio Domestico": 1,
    "Rifiuti ingombranti, RAEE, Legno, Sfalci e potature": 2,
    "Rifiuti Ingombranti": 2,
    "Rifiuti Ingombranti, RAEE": 2,
    "Rifiuti ingombranti, RAEE": 2,
    "Plastica": 3,
    "Carta": 4,
    "Cartone": 5,
    "Carta e Cartoni": 5,
    "Carta e Cartone": 5,
    "Cartone Selettivo": 5,
    "Vetro": 6,
    "Vetro e Metalli": 6,
    "Vetro e Alluminio": 6,
    "Metalli": 7,
    "Rifiuti urbani pericolosi, RAEE, Olio": 8,
    "Rifiuti Pericolosi": 8,
    "Indifferenziato": 9,
    "Secco Indifferenziato": 9,
    "Residuale": 9,
    "Plastica e Metalli": 10,
    "Plastica e Metallo": 10,
    "Plastica e Alluminio": 10,
    "Imballaggi Plastica e Metallici": 10,
    "Organico": 11,
    "Umido": 11,
    "Sfalci e Potature": 12,
    "Olio Vegetale Esausto": 13,
    "Abiti e Indumenti Usati": 14,
    "Pannolini e Pannoloni": 15,
    "Multimateriale": 16,
}
