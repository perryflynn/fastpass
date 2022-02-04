#!/usr/bin/env python3
# https://github.com/hannob/vacdec
# https://github.com/merlinschumacher/Open-Covid-Certificate-Validator

import sys
import zlib
import pprint

import base45
import cbor2
import cwt
from cwt import Claims
from pprint import pprint

from loader_de import CertificateLoader_DE

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

validatecertloader = CertificateLoader_DE()
validatecerts = validatecertloader()

def _decode(dcc):
    dcc = dcc.encode()
    if dcc.startswith(b'HC1:'):
        dcc = dcc[4:]
    try:
        dcc = base45.b45decode(dcc)
    except Exception as e:
        eprint(e)
        if (e is ValueError):
            return None

    if dcc.startswith(b'x'):
        try:
            dcc = zlib.decompress(dcc)
        except Exception as e:
            eprint(e)
            return None

    return dcc

def validate(dcc):
    dcc = _decode(dcc)
    if dcc is None:
        return [False, None]

    try:
        decoded = cwt.decode(dcc, keys=validatecerts)
        claims = Claims.new(decoded)
        return [True, claims.to_dict()]
    except Exception as e:
        try:
            decoded_noverify = cbor2.loads(dcc)
            decoded_noverify = cbor2.loads(decoded_noverify.value[2])
            eprint("Could not validate certificate.")
        except Exception as e:
            eprint("Could not decode certificate.")
            return [False, {}]

        return [False, decoded_noverify]

# get covid cert from stdin
cert = input()
eprint(f"Cert string: {cert}\n")

# verify and show result
pprint(validate(cert))
