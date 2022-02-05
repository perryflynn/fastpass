#!/usr/bin/env python3

from pprint import pprint
from fastpass.scan import scan_once
from fastpass.covcertvalidate import validate

certstr = scan_once('/dev/input/by-id/usb-NT_USB_Keyboard_6D14C8760000-event-kbd')

pprint(validate(certstr))
