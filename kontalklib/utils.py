# -*- coding: utf-8 -*-
'''Utilities and various constants.'''

USERID_LENGTH = 40
USERID_LENGTH_RESOURCE = 48

VALIDATION_CODE_LENGTH = 20

CHARSBOX_AZN_CASEINS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
CHARSBOX_AZN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz1234567890'
CHARSBOX_AZN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

import random, urllib2, base64, hashlib
from xml.etree import ElementTree

import database

# pyme
from pyme import core, callbacks
from pyme.constants.sig import mode

# init pyme
core.check_version(None)

def rand_str(length = 32, chars = CHARSBOX_AZN_CASEINS):
    # Length of character list
    chars_length = (len(chars) - 1)

    # Start our string
    string = chars[random.randrange(chars_length)]

    # Generate random string
    i = 1
    while i < length:
        # Grab a random character from our list
        r = chars[random.randrange(chars_length)]

        # Make sure the same two characters don't appear next to each other
        if r != string[i - 1]:
            string +=  r

        i = len(string)

    # Return the string
    return string

def sha1(text):
    hashed = hashlib.sha1(text)
    return hashed.hexdigest()

def xml_http_request(url, headers = {}):
    req = urllib2.Request(url=url, headers=headers)
    f = urllib2.urlopen(req)
    return ElementTree.parse(f)

def generate_node_token(rcpts, fp, text = None):
    if text == None:
        text = fp

    plain = core.Data(text)
    cipher = core.Data()
    ctx = core.Context()
    ctx.set_armor(0)

    # signing key
    ctx.signers_add(ctx.get_key(fp, True))
    # encrypting keys
    keys = []
    for r in rcpts:
        keys.append(ctx.get_key(r, False))

    ctx.op_encrypt_sign(keys, 1, plain, cipher)
    cipher.seek(0, 0)
    token = cipher.read()
    return base64.b64encode(token)

def verify_node_token(token, fp, text = None):
    # decode base64 first
    data = base64.b64decode(token)
    # setup pyme
    cipher = core.Data(data)
    plain = core.Data()
    ctx = core.Context()
    ctx.set_armor(0)

    ctx.op_decrypt_verify(cipher, plain)
    # check verification result
    res = ctx.op_verify_result()
    for sign in res.signatures:
        if sign.fpr == fp:
            plain.seek(0, 0)
            verify_fp = plain.read()
            check_text = text if text != None else fp
            if verify_fp == check_text:
                return check_text

    return None

def dict_get(data, key, default = None):
    return data[key] if key in data else default

def dict_get_none(data, key, default = None):
    return data[key] if key in data and data[key] != None else default

def db(config):
    cfg = config['database']
    return database.connect(
        cfg['host'], cfg['port'],
        cfg['user'], cfg['password'],
        cfg['dbname'], config['server'])
