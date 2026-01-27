import os
import json
from rest_framework.exceptions import ValidationError
from main.settings import BASE_DIR

JSON_PATH = os.path.join(BASE_DIR,
                         'api', 'data', "countries.json" )


def load_country_and_state():
    with open(JSON_PATH, "r", encoding="utf-8" ) as f :
        data  = json.load(f)

    return {
        item["country"].lower(): [s.lower() for s in item["states"]]
        for item in data
    }

COUNTRY_STATE_MAP = load_country_and_state()


def normalize(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


def validate_country_and_state(country, state):
    country = normalize(country).strip().lower()
    state =  normalize(state).strip().lower()

    print(type(country), country)
    print(type(state), state)
    if country not in COUNTRY_STATE_MAP:
        raise ValidationError({"message":" Country does not Exist"})
    pass

    if state not in COUNTRY_STATE_MAP[country]:
        raise ValidationError({"message" : " state is not a valid state in country "})