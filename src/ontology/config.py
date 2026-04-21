import json
import threading

from owlready2 import get_ontology, onto_path


onto_path.append('src/ontology/')
onto = get_ontology('db.owl').load()
sustainability = get_ontology('sustainability.owl').load()

_ID_FILE = './src/ontology/id.json'
_id_lock = threading.Lock()


def _read_ids() -> dict:
  with open(_ID_FILE, 'r') as fh:
    return json.load(fh)


def _write_ids(data: dict) -> None:
  with open(_ID_FILE, 'w') as fh:
    json.dump(data, fh)


def increase_id(obj: str) -> int:
  with _id_lock:
    data = _read_ids()
    data[obj] = data.get(obj, 0) + 1
    _write_ids(data)
    return data[obj]


def decrease_id(obj: str) -> int:
  with _id_lock:
    data = _read_ids()
    data[obj] = max(0, data.get(obj, 0) - 1)
    _write_ids(data)
    return data[obj]
