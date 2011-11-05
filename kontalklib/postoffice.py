# -*- coding: utf-8 -*-
'''Postoffice communication utilities.'''

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

    def _send(self, pack):
        box = BoxContainer()
        box.name = pack.__class__.__name__
        box.value = pack.SerializeToString()
        data = box.SerializeToString()
        self._conn.send(struct.pack(self.structFormat, len(data)) + data)

    def _recv(self):
        # TODO segmented receive
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
        print "waiting for response..."
        data = self._recv()
        print "got response!", data
        return self._extract(data[0], UsercacheLookupResponse)
