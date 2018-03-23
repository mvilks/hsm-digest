#!/usr/bin/env python3

import sys
import argparse
import PyKCS11


def parse_args():
    parser = argparse.ArgumentParser(description='Use hash function from specified library')
    parser.add_argument('-lib', choices=['softhsm', 'otlv'], required=True, help="PKCS#11 library to use")
    parser.add_argument('-pin', required=True, help="User PIN")
    return parser.parse_args()

def libs(lib):
    return {
        'softhsm': {
            'win32': 'C:\\SoftHSM2\\lib\\softhsm2.dll',
            'linux': '/usr/lib/softhsm/libsofthsm2.so'
        },
        'otlv': {
            'win32': 'C:\\Windows\\System32\\OTLvP11.dll',
            'linux': '/usr/lib/otlv-pkcs11.so'
        }
    }[lib][sys.platform]


if __name__ == '__main__':

    args = parse_args()
    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(libs(args.lib))

    slots = pkcs11.getSlotList(True)
    if len(slots) == 0:
        sys.exit('No slots available')

    session = pkcs11.openSession(slots[0], PyKCS11.CKF_RW_SESSION|PyKCS11.CKF_SERIAL_SESSION)
    session.login(args.pin)

    digests = {
        'a': '86f7e437faa5a7fce15d1ddcb9eaeaea377667b8',
        'ab': 'da23614e02469a0d7c7bd1bdab5c9c474b1904dc',
        'hello world!': '430ce34d020724ed75a196dfc2ad67c77772d169'
    }
    for key in digests:
        print('Calculating digest of string "%s"...' % key)
        print('  Using `session.digest(data)`: ')
        digest = session.digest(key)

        hex = "".join("%02x" % d for d in digest)
        if hex != digests[key]:
            print('  ✗ Wrong digest! %s' % hex)
        else:
            print('  ✓ OK: %s' % hex)

        print('  Using `session.digestSession().update(data).final()`: ')
        digest2 = session.digestSession().update(key).final()
        hex2 = "".join("%02x" % d for d in digest2)
        if hex2 != digests[key]:
            print('  ✗ Wrong digest! %s' % hex2)
        else:
            print('  ✓ OK: %s' % hex2)

    session.logout()
    
