# -*- coding: utf-8 -*-
'''Interface to messenger database.'''
'''
  Kontalk Pyserver2
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

import time, datetime
import logging as log
import oursql

import utils

from xml.sax.saxutils import escape


def connect_config(servercfg):
    config = servercfg['database']
    return connect(
        config['host'], config['port'],
        config['user'], config['password'],
        config['dbname'], servercfg['server']
    )

def connect(host, port, user, passwd, dbname, servercfg):
    log.debug("connecting to database %s on %s@%s" % (dbname, user, host))
    db = oursql.connect(host=host, port=port, user=user, passwd=passwd, db=dbname)
    return MessengerDb(db, servercfg)

def validations(mdb):
    return ValidationsDb(mdb._db, mdb._config)

def servers(mdb):
    return ServersDb(mdb._db, mdb._config)

def messages(mdb):
    return MessagesDb(mdb._db, mdb._config)

def usercache(mdb):
    return UsercacheDb(mdb._db, mdb._config)

def attachments(mdb):
    return AttachmentsDb(mdb._db, mdb._config)

# TODO other db instance creator helpers


def format_timestamp(ds):
    return ds.strftime('%Y-%m-%d %H:%M:%S')


class MessengerDb:
    '''Generic interface to messenger database.'''
    def __init__(self, db, config):
        self._config = config
        self._db = db

    def execute_update(self, query, args = ()):
        c = self._db.cursor()
        n = c.execute(query, args)
        c.close()
        return n

    def execute_query(self, query, args = ()):
        c = self._db.cursor(oursql.DictCursor)
        c.execute(query, args)
        return c

    def get_row(self, query, args = ()):
        c = self.execute_query(query, args)
        data = c.fetchone()
        c.close()
        return data

    def get_rows(self, query, args = ()):
        c = self.execute_query(query, args)
        data = c.fetchall()
        c.close()
        return data

    def get_rows_list(self, query, args = ()):
        c = self.execute_query(query, args)
        data = [row.values()[0] for row in c.fetchall()]
        c.close()
        return data

    def unlock(self):
        return self.execute_update('UNLOCK TABLES')


class ServersDb(MessengerDb):
    '''Interface to the servers table.'''
    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def get_address(self, fingerprint):
        r = self.get_row('SELECT address FROM servers WHERE fingerprint = ?', (fingerprint, ))
        if r:
            return r['address']

    def get_map(self, include_me = False):
        data = self.get_list(False, include_me)
        res = {}
        for row in data:
            res[row['fingerprint']] = (row['address'], row['serverlink'])
        return res

    def get_list(self, address_only = False, include_me = False):
        if not include_me:
            args = [ self._config['fingerprint'] ]
            extra = ' WHERE UPPER(fingerprint) <> UPPER(?)'
        else:
            args = None
            extra = ''

        if address_only:
            return self.get_rows_list('SELECT address FROM servers' + extra, args)
        else:
            return self.get_rows('SELECT * FROM servers' + extra, args)

    def get_keyring(self):
        return self.get_rows_list('SELECT fingerprint FROM servers')


class UsercacheDb(MessengerDb):
    '''Interface to the usercache table.'''
    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def get(self, userid, exact):
        q = 'SELECT * FROM usercache WHERE userid '
        if exact:
            q += '= ?'
            args = [ userid ]
        else:
            q += 'LIKE ?'
            args = [ userid + '%' ]

        return self.get_row(q + ' ORDER BY timestamp DESC', args)

    def get_generic(self, userid):
        q = 'SELECT * FROM usercache WHERE SUBSTR(userid, 1, ' + str(utils.USERID_LENGTH) + ') = ? ORDER BY timestamp DESC'
        return self.get_rows(q, (userid, ))

    def purge_old_entries(self):
        q = 'DELETE FROM usercache WHERE UNIX_TIMESTAMP() > (UNIX_TIMESTAMP(timestamp) + %d)' % (self._config['usercache.expire'])
        return self.execute_update(q)

    def update(self, userid, timestamp = None, **kwargs):
        args = [ userid ]
        cols = ['userid', 'timestamp']

        if timestamp:
            ts_str = '?'
            args.append(time.strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp)))
        else:
            ts_str = 'sysdate()'

        def add_field(args, cols, data, name):
            if data != None and len(data) == 0:
                data = None
            args.append(data)
            cols.append(name)

        if 'status' in kwargs:
            add_field(args, cols, kwargs['status'], 'status')
        if 'google_registrationid' in kwargs:
            add_field(args, cols, kwargs['google_registrationid'], 'google_registrationid')

        fmt = [ ts_str, ts_str]
        q = 'INSERT INTO usercache (%s) VALUES (?, %s%s)' % (', '.join(cols), ts_str, ',?' * (len(args) - 1))
        #log.debug('usercache(%s): %s' % (userid, q))
        try:
            return self.execute_update(q, args)
        except:
            fs = [ x + ' = ?' for x in cols[2:] ]
            fs.insert(0, 'timestamp = ' + ts_str)
            q = 'UPDATE usercache SET %s WHERE userid = ?' % ', '.join(fs)
            #log.debug('usercache(%s): %s' % (userid, q))
            return self.execute_update(q, args)

    def _entry_changed(self, old, new):
        return (
            # timeout expired
            (new['timestamp'] > (old['timestamp'] + self._config['usercache.validity']))
        )


class MessagesDb(MessengerDb):
    '''Interface to the messages table.'''
    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def lock(self, others = None):
        # for LOCK TABLES
        if (isinstance(others, tuple) or isinstance(others, list)) and len(others) > 0:
            extra = ',' + ' WRITE, '.join(others) + ' WRITE'
        else:
            extra = ''

        # for FLUSH TABLES
        if extra:
            extra2 = ',' + ','.join(others)
        else:
            extra2 = ''

        self.execute_update('LOCK TABLES messages WRITE' + extra)
        self.execute_update('FLUSH TABLES messages' + extra2)
        return True

    def get(self, msgid, resolve_group = False):
        '''Retrives a message.'''
        r = self.get_row('SELECT * FROM messages WHERE id = ?', (msgid, ))
        if r:
            g = r['group']
            if resolve_group and g:
                r['group'] = self.get_rows_list(
                    'SELECT recipient FROM messages WHERE `group` = ? AND `recipient` <> ?',
                    (g, r['recipient']))

        return r

    def get_multi(self, orig_id, resolve_group = False):
        '''Retrives multiple messages by orig_id.'''
        q = 'SELECT * FROM messages WHERE orig_id = ? ORDER BY timestamp'
        rs = self.get_rows(q, (orig_id, ))
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def get_count(self, orig_id):
        q = 'SELECT COUNT(orig_id) CNT FROM messages WHERE orig_id = %s'
        rs = self.get_row(q, (orig_id, ))
        return long(rs['CNT']) if rs else 0

    def generics(self, resolve_groups = False):
        '''Returns messages with generic recipient.'''
        q = 'SELECT * FROM messages WHERE LENGTH(recipient) = %d ORDER BY timestamp' % (utils.USERID_LENGTH)
        rs = self.get_rows(q)
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def need_notification(self, resolve_groups = False):
        '''Returns messages which need to be push notified.'''
        q = 'SELECT SUBSTR(recipient, 1, %d) recipient, COUNT(*) num \
            FROM messages GROUP BY SUBSTR(recipient, 1, %d)' % \
            (utils.USERID_LENGTH, utils.USERID_LENGTH)
        rs = self.get_rows(q)
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def pending(self, resolve_groups = False):
        '''Returns messages which need to be processed by the Postoffice.'''
        q = 'SELECT * FROM messages WHERE LENGTH(recipient) = %d ORDER BY timestamp' % \
            (utils.USERID_LENGTH)
        rs = self.get_rows(q)
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def incoming(self, userid, resolve_groups = False):
        '''Retrieves the list of incoming messages for a user.'''
        rs = self.get_rows('SELECT * FROM messages WHERE recipient = ? ORDER BY timestamp', (userid, ))
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def expired(self, resolve_groups = False):
        '''Returns expired messages (TTL <= 0).'''
        q = 'SELECT * FROM messages WHERE ttl <= 0'
        rs = self.get_rows(q)
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def resolve_groups(self, rs):
        for i, r in enumerate(rs):
            g = r['group']
            if g:
                rs[i]['group'] = self.get_rows_list(
                    'SELECT recipient FROM messages WHERE `group` = ? AND `recipient` <> ?',
                    [g, r['recipient']])

        return rs

    def delete(self, msgid):
        return self.execute_update('DELETE FROM messages WHERE id = ?', [ msgid ])

    def insert(self, id, timestamp, sender, recipient, group, mime, content, encrypted, filename, ttl, need_ack, orig_id = None):
        log.debug('using id: %s' % (id))

        args = [
            id,
            orig_id,
            timestamp,
            sender,
            recipient,
            group,
            mime,
            buffer(content),
            encrypted,
            filename,
            ttl,
            need_ack
        ]

        if self.execute_update('REPLACE INTO messages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', args):
            return True

        return False

    def insert2(self, msg):
        return self.insert(
            utils.dict_get(msg, 'id'),
            utils.dict_get(msg, 'timestamp'),
            utils.dict_get(msg, 'sender'),
            utils.dict_get(msg, 'recipient'),
            utils.dict_get_none(msg, 'group', None),
            utils.dict_get(msg, 'mime'),
            utils.dict_get(msg, 'content'),
            utils.dict_get_none(msg, 'encrypted', False),
            utils.dict_get(msg, 'filename'),
            utils.dict_get(msg, 'ttl'),
            utils.dict_get(msg, 'need_ack'),
            utils.dict_get(msg, 'orig_id')
        )

    def ttl_dec(self, msgid, count = 1):
        # FIXME there is some problem with formatting 'count' here...
        return self.execute_update("UPDATE messages SET ttl = ttl - %d WHERE id = ?" % (count), (msgid, ))

    def ttl_half(self, msgid):
        return self.execute_update("UPDATE messages SET ttl = ttl / 2 WHERE id = ?", (msgid,))


class ValidationsDb(MessengerDb):
    '''Interface to the validations table.'''

    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def get_code(self, userid):
        '''Retrieves a validation code from a userid.'''
        r = self.get_row('SELECT code FROM validations WHERE userid = ?', (userid, ))
        return r['code'] if r else False

    def get_userid(self, code):
        '''Retrieves the userid from a validation code.'''
        r = self.get_row('SELECT userid FROM validations WHERE code = ?', (code, ))
        return r['userid'] if r else False

    def delete(self, code):
        '''Deletes a validation code record.'''
        return self.execute_update('DELETE FROM validations WHERE code = ?', (code, ))

    def update(self, userid, code = False):
        '''Add/replace a validation record.'''
        if not code:
            code = utils.rand_str(utils.VALIDATION_CODE_LENGTH, utils.CHARSBOX_NUMBERS)
        fields = (userid, code)

        return (self.execute_update(
            'REPLACE INTO validations VALUES (?, ?)', fields),
            code
        )


class AttachmentsDb(MessengerDb):
    '''Interface to the attachments table.'''

    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def get(self, filename, userid = False):
        '''Retrieves an attachment entry, optionally filtering by user id.'''
        query = 'SELECT * FROM attachments WHERE filename = ?'
        args = [ filename ]
        if userid or userid == '':
            query += ' AND userid = ?'
            args.append(userid[:utils.USERID_LENGTH])

        return self.get_row(query, args)

    def insert(self, userid, filename, mime, md5sum):
        '''Inserts a new attachments entry.'''
        return self.execute_update('INSERT INTO attachments VALUES(?, ?, ?, ?)',
            (userid, filename, mime, md5sum))

    def delete(self, filename, userid = False):
        '''Deletes an attachment entry.'''
        query = 'DELETE FROM attachments WHERE filename = ?'
        args = [ filename ]
        if userid or userid == '':
            query += ' AND userid = ?'
            args.append(userid)

        return self.execute_update(query, args)
