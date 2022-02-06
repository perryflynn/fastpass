import sys
import zlib
import pprint

import base45
import cbor2
import cwt
from cwt import Claims
from pprint import pprint

from opencovid.loader_de import CertificateLoader_DE

from typing import Tuple

# https://github.com/hannob/vacdec
# https://github.com/merlinschumacher/Open-Covid-Certificate-Validator
# https://github.com/Digitaler-Impfnachweis/certification-apis/blob/master/dsc-update/README.md


class OpenCovidValidatorException(Exception):
    pass


def _decode(dcc):
    """ Decode covid certificate string """

    dcc = dcc.encode()
    if dcc.startswith(b'HC1:'):
        dcc = dcc[4:]
    try:
        dcc = base45.b45decode(dcc)
    except Exception as e:
        if (e is ValueError):
            return None

    if dcc.startswith(b'x'):
        try:
            dcc = zlib.decompress(dcc)
        except Exception as e:
            return None

    return dcc


def _load_certificates():
    """ Load certificates """

    validatecertloader = CertificateLoader_DE()
    return validatecertloader()


def validate(dcc: str) -> Tuple[bool, str, dict]:
    """ Validate a covid certificate string against certificate list """

    dcc = _decode(dcc)
    if dcc is None:
        return ( False, False, "Invalid format", None )

    validatecerts = _load_certificates()

    try:
        decoded = cwt.decode(dcc, keys=validatecerts)
        claims = Claims.new(decoded)
        return ( True, True, "Validated successfully", claims.to_dict() )
    except Exception as e:
        try:
            decoded_noverify = cbor2.loads(dcc)
            decoded_noverify = cbor2.loads(decoded_noverify.value[2])
            return ( True, False, "Unable to validate", decoded_noverify )
        except Exception as e:
            return ( False, False, "Unable to validate or decode", None )
