# -*- coding: utf-8 -*-
'''Utilities and various constants.'''
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

USERID_LENGTH = 40
USERID_LENGTH_RESOURCE = 48

# validation code length
VALIDATION_CODE_LENGTH = 6

# max length of user status message
STATUS_MESSAGE_MAX_LENGTH = 140

# default client port
DEFAULT_CLIENT_PORT = 6126
# default client http port
DEFAULT_CLIENT_HTTP_PORT = 6128
# default serverlink port
DEFAULT_SERVER_PORT = 6127

CHARSBOX_AZN_CASEINS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
CHARSBOX_AZN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz1234567890'
CHARSBOX_AZN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
CHARSBOX_NUMBERS = '1234567890'
CHARSBOX_HEX_LOWERCASE = 'abcdef1234567890'
CHARSBOX_HEX_UPPERCASE = 'ABCDEF1234567890'

import cPickle, pickle, os, shutil
import random, base64, hashlib
import Image, StringIO, vobject

from zope.interface import implements

# twisted web
from twisted.web import iweb
from twisted.cred import credentials, checkers, error
from twisted.python import failure
from twisted.internet import defer

import logging as log
import database, token

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
    Supported types: png, jpg, gif, vcard (vcf)
    """
    image_mimes = {
        'image/png' : 'PNG',
        'image/jpeg' : 'JPEG',
        'image/gif' : 'GIF'
    }

    if mime in image_mimes:
        im = Image.open(filename)
        im.thumbnail((128, 128), Image.ANTIALIAS)
        buf = StringIO.StringIO()
        im.save(buf, format=image_mimes[mime])
        return buf.getvalue()

    vcard_mimes = [
        'text/x-vcard',
        'text/vcard'
    ]
    if mime in vcard_mimes:
        f = open(filename, 'r')
        count = 0
        s = first = vobject.readComponents(f).next()
        while s:
            count += 1
            try:
                s = s.next()
            except:
                break
        if count > 1:
            return '%d vCard' % count
        else:
            return str(first.n.value).strip()

def generate_filename(mime):
    '''Generates a random filename for the given mime type.'''
    supported_mimes = {
        'image/png' : 'png',
        'image/jpeg' : 'jpg',
        'image/gif' : 'gif',
        'text/x-vcard' : 'vcf',
        'text/vcard' : 'vcf'
    }

    try:
        ext = supported_mimes[mime]
    except:
        # generic extension
        ext = 'bin'

    return 'att%s.%s' % (rand_str(6, CHARSBOX_AZN_LOWERCASE), ext)

def touch(fname, create = True):
        if os.path.exists(fname):
            os.utime(fname, None)
        elif create:
            open(fname, 'w').close()

def split_userid(userid):
    return userid[:USERID_LENGTH], userid[USERID_LENGTH:]

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f:
        for chunk in iter(lambda: f.read(128*md5.block_size), ''):
            md5.update(chunk)
    return md5.hexdigest()


## {{{ http://code.activestate.com/recipes/576642/ (r10)
class PersistentDict(dict):
    ''' Persistent dictionary with an API compatible with shelve and anydbm.

    The dict is kept in memory, so the dictionary operations run as fast as
    a regular dictionary.

    Write to disk is delayed until close or sync (similar to gdbm's fast mode).

    Input file format is automatically discovered.
    Output file format is selectable between pickle, json, and csv.
    All three serialization formats are backed by fast C implementations.

    '''

    def __init__(self, filename, flag='c', mode=None, *args, **kwds):
        self.flag = flag                    # r=readonly, c=create, or n=new
        self.mode = mode                    # None or an octal triple like 0644
        self.filename = filename
        if flag != 'n' and os.access(filename, os.R_OK):
            fileobj = open(filename, 'rb')
            with fileobj:
                self.load(fileobj)
        dict.__init__(self, *args, **kwds)

    def sync(self):
        '''Write dict to disk'''
        if self.flag == 'r':
            return
        filename = self.filename
        tempname = filename + '.tmp'
        fileobj = open(tempname, 'wb')
        try:
            if len(self) > 0:
                self.dump(fileobj)
        except Exception:
            os.remove(tempname)
            raise
        finally:
            fileobj.close()
        shutil.move(tempname, self.filename)    # atomic commit
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        self.sync()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    def dump(self, fileobj):
        cPickle.dump(dict(self), fileobj, pickle.HIGHEST_PROTOCOL)

    def load(self, fileobj):
        try:
            fileobj.seek(0)
            return self.update(cPickle.load(fileobj))
        except Exception:
            pass


class IKontalkToken(credentials.ICredentials):

    def checkToken():
        pass


class KontalkToken(object):
    implements(IKontalkToken)

    def __init__(self, token, fingerprint, keyring):
        self.token = token
        self.fingerprint = fingerprint
        self.keyring = keyring

    def checkToken(self):
        try:
            return token.verify_user_token(self.token, self.keyring, self.fingerprint)
        except:
            import traceback
            traceback.print_exc()
            log.debug("token verification failed!")


class AuthKontalkToken(object):
    implements(checkers.ICredentialsChecker)

    credentialInterfaces = IKontalkToken,

    def _cbTokenValid(self, userid):
        if userid:
            return userid
        else:
            return failure.Failure(error.UnauthorizedLogin())

    def requestAvatarId(self, credentials):
        return defer.maybeDeferred(
            credentials.checkToken).addCallback(
            self._cbTokenValid)


class AuthKontalkTokenFactory(object):
    implements(iweb.ICredentialFactory)

    scheme = 'kontalktoken'

    def __init__(self, fingerprint, keyring):
        self.fingerprint = fingerprint
        self.keyring = keyring

    def getChallenge(self, request):
        return {}

    def decode(self, response, request):
        key, token = response.split('=', 1)
        if key == 'auth':
            return KontalkToken(token, self.fingerprint, self.keyring)

        raise error.LoginFailed('Invalid token')
