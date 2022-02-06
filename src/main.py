#!/usr/bin/env python3

import os
import sys
import shutil
from click import getchar
import termcolor
import time
from pykeepass.exceptions import CredentialsError

from pprint import pprint
from fastpass.scan import scan_once
from fastpass.covcertvalidate import validate as covidvalidate
from fastpass.contactinfo import parse as contactinfoparse, passphraseparse
from fastpass.contactlist import ContactList

devaddr = '/dev/input/by-id/usb-NT_USB_Keyboard_6D14C8760000-event-kbd'

def loadbanner(file: str) -> str:
    with open(file, 'r') as f:
        return f.read()

def print_centered(text: str, vertical: bool = True, nonewline: bool = False, keep: int = 0):
    termsize = shutil.get_terminal_size((80, 40))

    if vertical:
        spacelines = termsize.lines - len(text.split('\n'))
        if spacelines > 0 and spacelines - keep > 0:
            for _ in range(0, int((spacelines-keep)/2)):
                print()

    if len(text.split('\n')) == 1 and nonewline:
        print(text.center(termsize.columns), end='')
    else:
        for line in text.split('\n'):
            print(line.center(termsize.columns))

    print('', end='', flush=True)

def clear():
    os.system('clear')

def pressanykey():
    print()
    print_centered("Drücke eine beliebige Taste... ", vertical=False, nonewline=True)
    getchar()

def main():
    question = loadbanner('banners/question.txt')
    success = loadbanner('banners/success.txt')
    failue = loadbanner('banners/failure.txt')
    saved = loadbanner('banners/saved.txt')
    lock = loadbanner('banners/lock.txt')

    # KeePass login
    clear()
    print_centered(termcolor.colored(lock, 'red'), keep=2)
    print()
    print_centered("Warte auf scan des KeePass Passphrase QR Codes...", vertical=False, nonewline=True)

    passphrase = passphraseparse(scan_once(devaddr))

    if not passphrase[0]:
        print("Not a valid passphrase QR Code! Exit.")
        sys.exit(1)

    cl = None
    try:
        cl = ContactList('../demo.kdbx')
        cl.open(passphrase[1])
        passphrase = None
    except CredentialsError:
        print("Wrong credentials! Exit.")
        sys.exit(1)

    # Wait for QR Codes
    while True:

        # wait-for-scan screen
        clear()
        print_centered(termcolor.colored(question, 'blue'), keep=2)
        print()
        print_centered("Warte auf QR Code scan...", vertical=False, nonewline=True)

        # start listening for scan string
        certstr = scan_once(devaddr)

        # try parse
        result = covidvalidate(certstr)
        contactinfo = contactinfoparse(certstr)

        clear()

        # covid cert
        if result['iscovidcert']:
            if result['status']:
                print_centered(termcolor.colored(success, 'green'), keep=5)
                print_centered(f"\n{result['info']['nam']['fnt']}, {result['info']['nam']['gnt']}\n{result['info']['dob']}", vertical = False)
                pressanykey()
            else:
                print_centered(termcolor.colored(failue, 'red'), keep=5)
                print_centered(f"\nUngültiges COVID Zertifikat\n(crypt: {result['cryptovalid']}; vac: {result['vaccinationstatus']}; euexp: {result['europeanexpired']})", vertical=False, nonewline=True)
                pressanykey()

        # contact info
        elif contactinfo[0]:
            if contactinfo[1]:
                cnumber, ctitle = cl.append(contactinfo[3])
                cl.save()

                if not cl.verify(ctitle):
                    print("ATTENTION! Failed to store contact!")

                print_centered(termcolor.colored(saved, 'green'), keep=7)
                print_centered(f"\n#{cnumber:05d}\n{contactinfo[3]['firstname']} {contactinfo[3]['lastname']}\n{contactinfo[3]['street']}\n{contactinfo[3]['city']}\n{contactinfo[3]['phone']}", vertical=False)

                pressanykey()
            else:
                print_centered(termcolor.colored(failue, 'red'), keep=5)
                print_centered(f"\nUngültiger Kontaktdaten QR Code\n({contactinfo[2]})", vertical=False, nonewline=True)
                pressanykey()

        # unknown
        else:
            print_centered(termcolor.colored("QR Code nicht erkannt.", 'red'))
            time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
