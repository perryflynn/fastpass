import base64
import json

def parse(infostr: str):
    try:
        jsonstr = base64.b64decode(infostr)
        data = json.loads(jsonstr)

        if not all(map(lambda x: x in data.keys(), [ 'city', 'firstname', 'lastname', 'phone', 'street' ])):
            return (True, False, "Properties missing", None)

        if not all(map(lambda x: isinstance(x, str), data.values())):
            return (True, False, "All properties must contain a string")

        if not all(map(lambda x: len(x.strip()) > 0, data.values())):
            return (True, False, "All properties must not empty")

        return (True, True, "Successfully parsed", data)
    except Exception:
        return (False, False, "Unable to parse", None)

def passphraseparse(passstr: str) -> str:
    try:
        jsonstr = base64.b64decode(passstr)
        data = json.loads(jsonstr)

        if data['passphrase'] and isinstance(data['passphrase'], str) and len(data['passphrase']) > 0:
            return (True, data['passphrase'])

        return (False, None)

    except Exception:
        return (False, None)
