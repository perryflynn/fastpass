# fastpass

**Project Status:** Covid check works, now make it fancy

Verify german COVID vaccination certificates and collect contact data.

## System dependencies

```sh
apt install python3 python3-wheel python3-setuptools rust-all
```

## Python 3 dependencies

```sh
cd src
pip install --no-cache-dir -r requirements.txt
```

## Technology

The following components are used for this project:

- [merlinschumacher/Open-Covid-Certificate-Validator](https://github.com/merlinschumacher/Open-Covid-Certificate-Validator) (AGPL 3.0)
- [hannob/vacdec](https://github.com/hannob/vacdec) (Unlicense)
