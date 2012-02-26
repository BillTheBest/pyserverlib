# -*- coding: utf-8 -*-
'''Postoffice communication utilities.'''
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

import socket, struct

from postoffice_pb2 import *


def connect(config):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(config['server']['postoffice.socket'])
    return Postoffice(s)


class Postoffice:
    """
    Postoffice communication class.
    Adapted from IntNStringReceiver from the Twisted Project:

    @ivar recvd: buffer holding received data when splitted.
    @type recvd: C{str}

    @ivar structFormat: format used for struct packing/unpacking. Define it in
        subclass.
    @type structFormat: C{str}

    @ivar prefixLength: length of the prefix, in bytes. Define it in subclass,
        using C{struct.calcSize(structFormat)}
    @type prefixLength: C{int}
    """

    MAX_LENGTH = 99999
    recvd = ""
    structFormat = "!I"
    prefixLength = struct.calcsize(structFormat)

    def __init__(self, conn):
        self._conn = conn

    def close(self):
        self._conn.close()

    def _send(self, pack):
        box = BoxContainer()
        box.name = pack.__class__.__name__
        box.value = pack.SerializeToString()
        data = box.SerializeToString()
        self._conn.send(struct.pack(self.structFormat, len(data)) + data)

    def _recv(self):
        recd = self._conn.recv(4096)
        packs = []
        self.recvd = self.recvd + recd
        while len(self.recvd) >= self.prefixLength: #and not self.paused:
            length ,= struct.unpack(
                self.structFormat, self.recvd[:self.prefixLength])
            if length > self.MAX_LENGTH:
                self._conn.close()
                return
            if len(self.recvd) < length + self.prefixLength:
                break
            packet = self.recvd[self.prefixLength:length + self.prefixLength]
            self.recvd = self.recvd[length + self.prefixLength:]
            packs.append(packet)

        return packs

    def _extract(self, data, klass):
        box = BoxContainer()
        box.ParseFromString(data)
        if box.name == klass.__name__:
            pack = klass()
            pack.ParseFromString(box.value)
            return pack

    def user_lookup(self, userid_list):
        req = UsercacheLookupRequest()
        req.user_id.extend(userid_list)
        self._send(req)
        #print "waiting for response..."
        data = self._recv()
        #print "got response!", data
        return self._extract(data[0], UsercacheLookupResponse)

    def message_queue(self, userid = None):
        req = MessageQueueRequest()
        if userid:
            req.user_id = userid
        self._send(req)
        # postoffice-driven polling requested - wait for response
        if userid:
            #print "waiting for response..."
            data = self._recv()
            #print "got response!", data
            return self._extract(data[0], MessageQueueResponse)
