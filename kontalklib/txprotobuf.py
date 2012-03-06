# -*- coding: utf-8 -*-
'''Google Protocol Buffers Twisted protocol.'''
'''
  Kontalk pyserver2
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

from twisted.protocols.basic import Int32StringReceiver

from txprotobuf_pb2 import BoxContainer
import utils


class Protocol(Int32StringReceiver):

    # TODO define MAX_LENGTH

    def __init__(self, modules):
        self._modules = modules

    def stringReceived(self, data):
        box = BoxContainer()
        box.ParseFromString(data)
        if box.name != "":
            out_klass = getattr(self._modules, box.name)
            out = out_klass()
            if box.value != "":
                out.ParseFromString(box.value)
            self.boxReceived(out, box.tx_id)

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

    def sendBox(self, data, tx_id = None):
        box = BoxContainer()
        box.name = data.__class__.__name__
        box.value = data.SerializeToString()
        # generate random tx id if not given
        if not tx_id:
            tx_id = utils.rand_str(8)
        box.tx_id = tx_id
        self.sendString(box.SerializeToString())

    def boxReceived(self, data, tx_id = None):
        raise NotImplementedError
