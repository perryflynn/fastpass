# fastpass

Verify german COVID vaccination certificates and collect contact data on events.

**Project Status:** First prototype, please test!

## Features

- Works offline with PC + QR Code scanner
- Contact data collection in KeePass database from QR Code
- Database unlock with passphrase QR Code
- Check COVID vaccination certificates

## System dependencies

```sh
apt install python3 python3-wheel python3-setuptools rust-all
```

## Python 3 dependencies

```sh
cd src
pip install --no-cache-dir -r requirements.txt
```

## Installation

- Install dependencies
- Create KeePass DB in this directory as `demo.kdbx` (will be configurable in future)
- Generate QR Code for passphrase

```sh
# qrencode is included in ubuntu package repos
# passphrase as json, base64 encoded
echo '{ "passphrase": "Yei3aphah8aebeimee6oiv4e" }' | base64 -w0 | qrencode -t UTF8 -o -
```

- Adjust scanner device path in `main.py` (will be configurable in future)

```py
devaddr = '/dev/input/by-id/usb-NT_USB_Keyboard_6D14C8760000-event-kbd'
```

## Start

- Start script

```sh
cd src/
python3 main.py
```

- Unlock KeePass database by scanning passphrase QR Code

## Contact data

The scanner expects a QR Code in the following format:

```sh
# qrencode is included in ubuntu package repos
# base64 encoded json
echo '{ "city":"", "firstname":"", "lastname":"", "phone":"", "street":" " }' | base64 -w0 | qrencode -o - -t UTF8
```

Web App for event visitors to generate that QR Code client-side:

[https://kontakt.lan.mudkips.de/](https://kontakt.lan.mudkips.de/)

## Technology

The following components are used for this project:

- [merlinschumacher/Open-Covid-Certificate-Validator](https://github.com/merlinschumacher/Open-Covid-Certificate-Validator) (AGPL 3.0)
- [hannob/vacdec](https://github.com/hannob/vacdec) (Unlicense)
- [HerrSpace/CCC-Membership-Form](https://github.com/HerrSpace/CCC-Membership-Form) (MIT License)
