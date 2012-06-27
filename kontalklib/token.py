# -*- coding: utf-8 -*-
'''Token functions.'''
'''
  Kontalk Pyserver
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

import utils

# pyme
from pyme import core, callbacks
from pyme.constants.sig import mode

import base64

def user_token(userid, fp):
    '''Generates a user token.'''

    '''
    token is made up of the hashed phone number (the user id)
    plus the resource (in one big string, 40+8 characters),
    and the fingerprint of the server he registered to
    '''
    string = '%s|%s' % (userid, fp)
    plain = core.Data(string)
    cipher = core.Data()
    ctx = core.Context()
    ctx.set_armor(0)

    # signing key
    ctx.signers_add(ctx.get_key(fp, True))

    ctx.op_sign(plain, cipher, mode.NORMAL)
    cipher.seek(0, 0)
    token = cipher.read()
    return base64.b64encode(token)

def verify_user_token(token, serversdb, fp = None):
    '''Verifies a user token against a single fingerprint or the keyring.'''

    # decode base64 first
    data = base64.b64decode(token)
    # setup pyme
    cipher = core.Data(data)
    plain = core.Data()
    ctx = core.Context()
    ctx.set_armor(0)

    ctx.op_verify(cipher, None, plain)
    # check verification result
    res = ctx.op_verify_result()
    if len(res.signatures) > 0:
        sign = res.signatures[0]
        plain.seek(0, 0)
        text = plain.read()
        data = text.split('|', 2)

        # not a valid token
        if len(data) != 2:
            return None

        # length not matching - refused
        userid = data[0]
        if len(userid) != utils.USERID_LENGTH_RESOURCE:
            return None

        # compare with provided fingerprint (if any)
        if fp and (sign.fpr.upper() == fp.upper()):
            return userid

        # no match - compare with keyring
        keyring = serversdb.get_keyring()
        for key in keyring:
            if sign.fpr.upper() == key.upper():
                return userid

    return None
