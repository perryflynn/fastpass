import time

from opencovid.validator import validate as openvalidate
from pprint import pprint

def validate(certstr: str) -> dict:
    """ Check covid certificate rules """

    result = openvalidate(certstr)

    response = {
        'status': False,
        'cryptovalid': result[0],
        'cryptovalidmsg': result[1],
        'info': None,
        'issuer': None,
        'vaccinationstatus': None,
        'notvalidyet': None,
        'expired': None,
        'timerangeerror': None,
    }

    # check if these weird outline fields exist
    keychecks = (
        # certinfo
        -260 in result[2].keys() and 1 in result[2][-260]
        # country and time range
        and 1 in result[2].keys() and 4 in result[2].keys() and 6 in result[2].keys()
    )

    if not keychecks:
        response['statusmsg'] = 'Certificate content is malformed.'
        return response

    # check certificate contents
    info = result[2][-260][1]
    response['info'] = info
    response['issuer'] = result[2][1]

    # check vaccination status
    response['vaccinationstatus'] = info['v'][0]['dn'] >= info['v'][0]['sd']

    # time range
    # https://datatracker.ietf.org/doc/html/rfc8392#section-3.1.4
    # 4 = expiration
    # 5 = not before
    # 6 = issued at
    tsnow = int(time.time())
    tsexpire = result[2][4]
    tsissued = result[2][6]

    response['timerangeerror'] = tsexpire <= tsissued
    response['notvalidyet'] = tsissued < tsexpire and tsnow < tsissued
    response['expired'] = tsissued < tsexpire and tsnow > tsexpire

    # overall status
    response['status'] = (
        response['cryptovalid']
        and response['vaccinationstatus']
        and not response['timerangeerror']
        and not response['notvalidyet']
        and not response['expired']
    )

    return response
