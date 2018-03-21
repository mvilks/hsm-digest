# HSM Digest

## Prerequisites

* Python 3
* [PyKCS11](https://github.com/LudovicRousseau/PyKCS11)
* [eParakstītājs 3.0](https://www.eparaksts.lv/lv/lejupielades) ([eID-LV Middleware](https://github.com/eID-LV/Middleware))
* [SoftHSM2](https://www.opendnssec.org/download/)

## Digests

### Running

Using SoftHSM2:
```
python digest.py -lib softhsm -pin 0000
```

Using eID LV Middleware:
```
python digest.py -lib otlv -pin 0000
```

### Results
This program uses SHA1 (default) hash function to get digest of three strings.
Digests can be checked individually against `sha1sum` tool:
```
echo -n "hello world!" | sha1sum
```
The wrong digests that eID LV Middleware gives are calculated from twice repeated string:
```
echo -n "hello world!hello world!" | sha1sum
```

So far I have no clue why that's so.

