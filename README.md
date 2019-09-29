### Obsolete

> *Starting from version 2.0.4 of [`latvia-eid-middleware`](https://download.eparaksts.lv/files/ep3updates/debian/dists/bionic/eparaksts/binary-amd64/Packages) digest functions have been fixed and now return correct values using both digest methods.*

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

[PKCS#11](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html#_Toc416959746) defines two similar approaches to using message digest functions: using `C_Digest` or `C_DigestUpdate` + `C_DigestFinal`:
 > **C\_Digest** is equivalent to a sequence of **C\_DigestUpdate** operations followed by **C\_DigestFinal**.

It appears only `C_Digest` function in eID LV Middleware gives wrong digests.

