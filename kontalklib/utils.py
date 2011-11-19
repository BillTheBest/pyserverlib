# -*- coding: utf-8 -*-
'''Utilities and various constants.'''
'''
  Kontalk Android client
  Copyright (C) 2011 Kontalk Devteam <devteam@kontalk.org>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

USERID_LENGTH = 40
USERID_LENGTH_RESOURCE = 48

VALIDATION_CODE_LENGTH = 20

CHARSBOX_AZN_CASEINS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
CHARSBOX_AZN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz1234567890'
CHARSBOX_AZN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

import random, base64, hashlib
import Image, StringIO

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

def generate_preview_content(filename, mime):
    """
    Creates a preview content for the given file and mime type.
    Supported types: png, jpg, gif
    """
    supported_mimes = {
        'image/png' : 'PNG',
        'image/jpeg' : 'JPEG',
        'image/gif' : 'GIF'
    }

    if mime in supported_mimes:
        im = Image.open(filename)
        im.thumbnail((128, 128), Image.ANTIALIAS)
        buf = StringIO.StringIO()
        im.save(buf, format=supported_mimes[mime])
        return buf.getvalue()

def generate_filename(mime):
    '''Generates a random filename for the given mime type.'''
    supported_mimes = {
        'image/png' : 'png',
        'image/jpeg' : 'jpg',
        'image/gif' : 'gif'
    }

    try:
        ext = supported_mimes[mime]
    except:
        # generic extension
        ext = 'bin'

    return 'att%s.%s' % (rand_str(6, CHARSBOX_AZN_LOWERCASE), ext)
