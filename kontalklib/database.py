# -*- coding: utf-8 -*-
'''Interface to messenger database.'''

import time
import logging as log
import MySQLdb

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
    db = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=dbname)
    return MessengerDb(db, servercfg)


class MessengerDb:
    '''Generic interface to messenger database.'''
    def __init__(self, db, config):
        self._config = config
        self._db = db
        self._db.autocommit(True)

    def servers(self):
        '''Returns a reference to a new ServerDb instance.'''
        return ServersDb(self._db, self._config)

    def usercache(self):
        '''Returns a reference to a new UsercacheDb instance.'''
        return UsercacheDb(self._db, self._config)

    def messages(self):
        '''Returns a reference to a new MessagesDb instance.'''
        return MessagesDb(self._db, self._config)

    def validations(self):
        '''Returns a reference to a new ValidationsDb instance.'''
        return ValidationsDb(self._db, self._config)

    def attachments(self):
        '''Returns a reference to a new AttachmentsDb instance.'''
        return AttachmentsDb(self._db, self._config)

    def execute_update(self, query, args = None):
        c = self._db.cursor()
        n = c.execute(query, args)
        c.close()
        return n

    def execute_query(self, query, args = None):
        c = self._db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        c.execute(query, args)
        return c

    def get_row(self, query, args = None):
        c = self.execute_query(query, args)
        data = c.fetchone()
        c.close()
        return data

    def get_rows(self, query, args = None):
        c = self.execute_query(query, args)
        data = c.fetchall()
        c.close()
        return data

    def get_rows_list(self, query, args = None):
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
        r = self.get_row('SELECT address FROM servers WHERE fingerprint = %s', (fingerprint, ))
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
            extra = ' WHERE UPPER(fingerprint) <> UPPER(%s)'
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
            q += '= %s'
            args = [ userid ]
        else:
            q += 'LIKE %s'
            args = [ userid + '%' ]

        return self.get_row(q + ' ORDER BY timestamp DESC', args)

    def get_generic(self, userid):
        q = 'SELECT * FROM usercache WHERE SUBSTR(userid, 1, ' + str(utils.USERID_LENGTH) + ') = %s ORDER BY timestamp DESC'
        return self.get_rows(q, [ userid ])

    def purge_old_entries(self):
        q = 'DELETE FROM usercache WHERE UNIX_TIMESTAMP() > (UNIX_TIMESTAMP(timestamp) + %d)' % (self._config['usercache.expire'])
        return self.execute_update(q)

    def update(self, userid, timestamp = None, google_regid = None):
        args = { 'userid' : userid }

        if timestamp:
            ts_str = '%(timestamp)s'
            args['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp))
        else:
            ts_str = 'sysdate()'

        q = 'INSERT INTO usercache (userid, timestamp) VALUES (%%(userid)s, %s) ON DUPLICATE KEY UPDATE timestamp = %s' % (ts_str, ts_str)
        return self.execute_update(q, args)

    def update_field(self, userid, field, value):
        q = 'UPDATE usercache SET %s = %%s WHERE userid = %%s' % (field)
        return self.execute_update(q, (value, userid))

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
        r = self.get_row('SELECT * FROM messages WHERE id = %s', (msgid, ))
        if r:
            g = r['group']
            if resolve_group and g:
                r['group'] = self.get_rows_list(
                    'SELECT recipient FROM messages WHERE `group` = %s AND `recipient` <> %s',
                    (g, r['recipient']))

        return r

    def generics(self, resolve_groups = False):
        '''Returns messages with generic recipient.'''
        q = 'SELECT * FROM messages WHERE LENGTH(recipient) = ' + str(utils.USERID_LENGTH)
        rs = self.get_rows(q)
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def pending(self, resolve_groups = False):
        '''Returns messages which need to be processed by the Postoffice.'''
        q = 'SELECT * FROM messages WHERE (LENGTH(recipient) = %d\
 AND remote_lock IS NULL AND local_lock IS NULL)\
 OR (LENGTH(recipient) = %d AND\
 ( (local_lock IS NULL) = (remote_lock IS NULL) OR\
 ((remote_lock IS NULL OR UNIX_TIMESTAMP() > (UNIX_TIMESTAMP(remote_lock) + %d))\
 AND (local_lock IS NULL OR UNIX_TIMESTAMP() > (UNIX_TIMESTAMP(local_lock) + %d)))))' % \
            (utils.USERID_LENGTH, utils.USERID_LENGTH_RESOURCE,
             self._config['message.lock_validity'], self._config['message.lock_validity'])
        rs = self.get_rows(q)
        if resolve_groups:
            self.resolve_groups(rs)
        return rs

    def incoming(self, userid, local_lock = False, remote_lock = False, resolve_groups = False):
        '''Retrieves the list of incoming message for a user.'''
        extra = ''
        fields = {
            # FIXME handle resources
            'userid' : userid
        }

        if local_lock == None:
            extra = ' AND local_lock IS NULL'
        elif local_lock == True:
            extra = ' AND local_lock IS NOT NULL'
        elif local_lock == 1:
            extra = ' AND unix_timestamp() > (unix_timestamp(local_lock) + ' + self._config['message.lock_validity'] + ')'

        if remote_lock == None:
            extra = ' AND remote_lock IS NULL'
        elif remote_lock == True:
            extra = ' AND remote_lock IS NOT NULL'
        elif remote_lock == 1:
            extra = ' AND unix_timestamp() > (unix_timestamp(remote_lock) + ' + self._config['message.lock_validity'] + ')'

        # FIXME handle resources
        rs = self.get_rows('SELECT * FROM messages WHERE recipient = %(userid)s' + extra, fields)
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
                    'SELECT recipient FROM messages WHERE `group` = %s AND `recipient` <> %s',
                    [g, r['recipient']])

        return rs

    def clean_locks(self):
        '''Cleans remote_lock on generic messages.'''
        return self.execute_update('UPDATE messages SET remote_lock = NULL WHERE LENGTH(recipient) = %d' % \
            utils.USERID_LENGTH)

    def delete(self, msgid):
        return self.execute_update('DELETE FROM messages WHERE id = %s', [ msgid ])

    def insert(self, id, sender, recipient, group, mime, content, encrypted, filename, ttl, orig_id = None, local_lock = False, remote_lock = False):
        if not id:
            id = self.generate_id()

        log.debug('using id: %s' % (id))

        args = [
            id,
            orig_id,
            sender,
            recipient,
            group,
            mime,
            content,
            encrypted,
            filename,
            ttl
        ]

        local = 'sysdate()' if local_lock else 'NULL'
        remote = 'sysdate()' if remote_lock else 'NULL'

        if self.execute_update('INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '+local+', '+remote+')', args):
            return id

        return False

    def insert2(self, msg):
        return self.insert(
            utils.dict_get(msg, 'id'),
            utils.dict_get(msg, 'sender'),
            utils.dict_get(msg, 'recipient'),
            utils.dict_get_none(msg, 'group', None),
            utils.dict_get(msg, 'mime'),
            utils.dict_get(msg, 'content'),
            utils.dict_get_none(msg, 'encrypted', False),
            utils.dict_get(msg, 'filename'),
            utils.dict_get(msg, 'ttl'),
            utils.dict_get(msg, 'orig_id'),
            utils.dict_get_none(msg, 'local_lock', False),
            utils.dict_get_none(msg, 'remote_lock', False)
        )

    def ttl_dec(self, msgid, count = 1):
        # FIXME there is some problem with formatting 'count' here...
        return self.execute_update("UPDATE messages SET ttl = ttl - " +
            str(count) + " WHERE id = %s", (msgid, ))

    def ttl_half(self, msgid):
        return self.execute_update("UPDATE messages SET ttl = ttl / 2 WHERE id = %s", (msgid,))

    def local_lock(self, msgid, clear = False):
        what = 'NULL' if clear else 'sysdate()'
        return self.execute_update('UPDATE messages SET local_lock = ' + what + ' WHERE id = %s', (msgid, ))

    def remote_lock(self, msgid, clear = False):
        what = 'NULL' if clear else 'sysdate()'
        return self.execute_update('UPDATE messages SET remote_lock = ' + what + ' WHERE id = %s', (msgid, ))

    def ttl_dec_for_local_lock(self, msgid):
        return self.execute_update('UPDATE messages SET remote_lock = NULL, local_lock = sysdate(), ttl = ttl - 1 WHERE id = %s',
            (msgid, ))

    def generate_id(self):
        # TODO %z is deprecated
        return self._config['fingerprint'] + time.strftime('%Y%m%d%H%M%S%z') + utils.rand_str(5, utils.CHARSBOX_AZN_UPPERCASE)

    def message_receipt(self, msgid, status, sender = None, recipient = None):
        return {
            'sender' : sender,
            'recipient' : recipient,
            'content' : '<r><i>%s</i><e>%d</e></r>' % (escape(msgid), status),
            'mime' : 'r',
            'ttl' : self._config['ttl.receipt']
        }


class ValidationsDb(MessengerDb):
    '''Interface to the validations table.'''

    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def get_code(self, userid):
        '''Retrieves a validation code from a userid.'''
        r = self.get_row('SELECT code FROM validations WHERE userid = %s', (userid, ))
        return r['code'] if r else False

    def get_userid(self, code):
        '''Retrieves the userid from a validation code.'''
        r = self.get_row('SELECT userid FROM validations WHERE code = %s', (code, ))
        return r['userid'] if r else False

    def delete(self, code):
        '''Deletes a validation code record.'''
        return self.execute_update('DELETE FROM validations WHERE code = %s', (code, ))

    def update(self, userid, code = False):
        '''Add/replace a validation record.'''
        if not code:
            code = utils.rand_str(utils.VALIDATION_CODE_LENGTH, utils.CHARSBOX_AZN_UPPERCASE)
        fields = (userid, code)

        return (self.execute_update(
            'REPLACE INTO validations VALUES (%s, %s)', fields),
            code
        )


class AttachmentsDb(MessengerDb):
    '''Interface to the attachments table.'''

    def __init__(self, db, config):
        MessengerDb.__init__(self, db, config)

    def get(self, filename, userid = False):
        '''Retrieves an attachment entry, optionally filtering by user id.'''
        query = 'SELECT * FROM attachments WHERE filename = %s'
        args = [ filename ]
        if userid:
            query += ' AND userid = %s'
            args.append(userid)

        return self.get_row(query, args)

    def insert(self, userid, filename, mime):
        '''Inserts a new attachments entry.'''
        return self.execute_update('INSERT INTO attachments VALUES(%s, %s, %s)',
            (userid, filename, mime))

    def delete(self, filename):
        '''Deletes an attachment entry.'''
        return self.execute_update('DELETE FROM attachments WHERE filename = %s', (filename, ))
