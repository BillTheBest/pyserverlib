# -*- coding: utf-8 -*-
'''Google Protocol Buffers Twisted protocol.'''
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

from StringIO import StringIO
from twisted.internet import protocol

# HACK importing non-exposed modules
from google.protobuf.internal import encoder, decoder

from txprotobuf_pb2 import BoxContainer
import utils


class Protocol(protocol.Protocol):
    # max size: 1 MB
    MAX_LENGTH = 1048576
    # temporary buffer
    _buf = ''
    # length of future-coming data
    _length = -1
    # overflow length
    _over_length = -1

    def __init__(self, modules):
        self._modules = modules

    def dataReceived(self, data):
        # ignoring data
        if self._over_length >= 0:
            if data:
                #print "got %d bytes of extra data" % len(data)
                self._over_length += len(data)
            # ignored data reached, keep the rest
            #print "ignoring %d/%d bytes" % (self._over_length, self._length)
            if self._over_length >= self._length:
                diff = (self._length - self._over_length)
                self._buf = data[diff:] if diff > 0 else ''
                # cancel incoming buffer since we already appended it
                data = None
                self._over_length = -1
                self._length = -1
                #print "ignore limit reached - keeping %d bytes" % len(self._buf)
            else:
                # do not continue with parsing
                return

        if data:
            self._buf += data
        #print "length-before:", len(self._buf)
        # no data received yet
        if self._length < 0 and self._buf:
            #print "parsing length..."
            length, length_len = decoder._DecodeVarint32(self._buf, 0)
            #print [length, length_len]
            self._length = length
            # remove length's length from buffer and continue reading
            self._buf = self._buf[length_len:]
            #print "length-after:", len(self._buf)

            # data is too big - drop buffer and ignore the rest
            if length > self.MAX_LENGTH:
                print "too much data - ignoring"
                self._over_length = len(self._buf)
                self._buf = ''
                return

        if self._length > 0 and len(self._buf) >= self._length and self._over_length < 0:
            #print "length %d reached (%d)" % (self._length, len(self._buf))
            out = self._buf[:self._length]
            #print "out data %d" % len(out)
            self.stringReceived(out)
            # don't forget the next pack :)
            self._buf = self._buf[self._length:]
            self._length = -1
            if self._buf:
                self.dataReceived(None)

    def sendString(self, string):
        #print "sending %d bytes" % len(string)
        out = StringIO()
        encoder._EncodeVarint(out.write, len(string))
        out.write(string)
        self.transport.write(out.getvalue())

    def stringReceived(self, data):
        box = BoxContainer()
        box.ParseFromString(data)
        if box.name != "":
            out_klass = getattr(self._modules, box.name)
            out = out_klass()
            if box.value != "":
                out.ParseFromString(box.value)
            self.boxReceived(out, box.tx_id)

    """
    FIXME this might not work
    def sendBoxes(self, datas, tx_id = None):
        # generate random tx id if not given
        if not tx_id:
            tx_id = utils.rand_str(8)
        buf = ''
        for data in datas:
            box = BoxContainer()
            box.name = data.__class__.__name__
            box.value = data.SerializeToString()
            box.tx_id = tx_id
            buf += box.SerializeToString()
        self.sendString(buf)
    """

    def sendBox(self, data, tx_id = None):
        box = BoxContainer()
        box.name = data.__class__.__name__
        box.value = data.SerializeToString()
        # generate random tx id if not given
        if not tx_id:
            tx_id = utils.rand_str(8)
        box.tx_id = tx_id
        self.sendString(box.SerializeToString())
        return tx_id

    def boxReceived(self, data, tx_id = None):
        raise NotImplementedError
