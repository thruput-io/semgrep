import pickle
import yaml
import json

def load_payload(raw_data):
    # ruleid: python-insecure-deserialization
    obj1 = pickle.loads(raw_data)

    # ruleid: python-insecure-deserialization
    obj2 = yaml.load(raw_data)

    # ruleid: python-insecure-deserialization
    obj3 = yaml.load(raw_data, Loader=yaml.Loader)

    # ok: python-insecure-deserialization
    obj4 = yaml.safe_load(raw_data)

    # ok: python-insecure-deserialization
    obj5 = json.loads(raw_data)

    return obj1, obj2, obj3, obj4, obj5
