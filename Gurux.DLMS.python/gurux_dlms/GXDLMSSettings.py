#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .enums import Priority, ServiceClass, InterfaceType, Authentication, Standard, HdlcFrameType, Conformance
from .ConnectionState import ConnectionState
from .objects.GXDLMSObjectCollection import GXDLMSObjectCollection
from .GXDLMSLimits import GXDLMSLimits

#
# This class includes DLMS communication settings.
# pylint: disable=too-many-public-methods,too-many-instance-attributes
#
class GXDLMSSettings:
    #
    # Server sender frame sequence starting number.
    #
    __SERVER_START_SENDER_FRAME_SEQUENCE = 0x1E

    #
    # Server receiver frame sequence starting number.
    #
    __SERVER_START_RECEIVER_FRAME_SEQUENCE = 0xEE

    #
    # Client sender frame sequence starting number.
    #
    __CLIENT_START_SENDER_FRAME_SEQUENCE = 0x10

    #
    # Client receiver frame sequence starting number.
    #
    __CLIENT_START_RCEIVER_FRAME_SEQUENCE = 0xE

    #
    # DLMS version number.
    #
    __DLMS_VERSION = 6
    __MAX_RECEIVE_PDU_SIZE = 0xFFFF

    @classmethod
    def getInitialConformance(cls, useLogicalNameReferencing):
        if useLogicalNameReferencing:
            return Conformance.BLOCK_TRANSFER_WITH_ACTION | Conformance.BLOCK_TRANSFER_WITH_SET_OR_WRITE | Conformance.BLOCK_TRANSFER_WITH_GET_OR_READ | Conformance.SET | Conformance.SELECTIVE_ACCESS | Conformance.ACTION | Conformance.MULTIPLE_REFERENCES | Conformance.GET
        return Conformance.INFORMATION_REPORT | Conformance.READ | Conformance.UN_CONFIRMED_WRITE | Conformance.WRITE | Conformance.PARAMETERIZED_ACCESS | Conformance.MULTIPLE_REFERENCES

    #
    # Constructor.
    #
    def __init__(self, isServer):
        self.skipFrameCheck = False
        self.customChallenges = False
        self.ctoSChallenge = None
        self.stoCChallenge = None
        self.sourceSystemTitle = None
        self.invokeId = 0x1
        self.longInvokeID = 0x1
        self.priority = Priority.HIGH
        self.serviceClass = ServiceClass.CONFIRMED
        self.clientAddress = 16
        self.serverAddress = 1
        self.serverAddressSize = 1
        self.useLogicalNameReferencing = True
        self.interfaceType = InterfaceType.HDLC
        self.authentication = Authentication.NONE
        self.password = None
        self.kek = None
        self.count = 0
        self.index = 0
        self.targetEphemeralKey = None
        self.dlmsVersion = self.__DLMS_VERSION
        self.connected = ConnectionState.NONE
        self.allowAnonymousAccess = False
        self.maxPduSize = self.__MAX_RECEIVE_PDU_SIZE
        self.maxServerPDUSize = self.__MAX_RECEIVE_PDU_SIZE
        self.startingPacketIndex = 1
        # Gets current block index.
        self.blockIndex = 1
        self.cipher = None
        self.blockNumberAck = 0
        self.protocolVersion = None
        self.isServer = isServer
        self.objects = GXDLMSObjectCollection()
        self.limits = GXDLMSLimits()
        self.gateway = None
        self.proposedConformance = GXDLMSSettings.getInitialConformance(self.useLogicalNameReferencing)
        self.resetFrameSequence()
        self.windowSize = 1
        self.userId = -1
        #Quality of service.
        self.qualityOfService = 0
        self.useUtc2NormalTime = False
        self.standard = Standard.DLMS
        self.negotiatedConformance = Conformance.NONE
        self.invokeID = 0
        self.receiverFrame = 0
        self.senderFrame = 0

    #
    # Client to Server challenge.
    #
    def getCtoSChallenge(self):
        return self.ctoSChallenge

    #
    # @param value
    # Client to Server challenge.
    #
    def setCtoSChallenge(self, value):
        if not self.customChallenges or self.ctoSChallenge is None:
            self.ctoSChallenge = value

    #
    # Server to Client challenge.
    #
    def getStoCChallenge(self):
        return self.stoCChallenge

    #
    # @param value
    # Server to Client challenge.
    #
    def setStoCChallenge(self, value):
        if not self.customChallenges or self.stoCChallenge is None:
            self.stoCChallenge = value

    #
    # Is connection accepted.
    #
    def acceptConnection(self):
        return self.connected != ConnectionState.NONE or self.allowAnonymousAccess or (self.cipher and self.cipher.sharedSecret)

    #
    # Reset frame sequence.
    #
    def resetFrameSequence(self):
        if self.isServer:
            self.senderFrame = self.__SERVER_START_SENDER_FRAME_SEQUENCE
            self.receiverFrame = self.__SERVER_START_RECEIVER_FRAME_SEQUENCE
        else:
            self.senderFrame = self.__CLIENT_START_SENDER_FRAME_SEQUENCE
            self.receiverFrame = self.__CLIENT_START_RCEIVER_FRAME_SEQUENCE

    #pylint: disable=too-many-return-statements
    def checkFrame(self, frame_):
        #  If notify
        if frame_ == 0x13:
            return True
        #  If U frame.
        if (frame_ & HdlcFrameType.U_FRAME.value) == HdlcFrameType.U_FRAME.value:
            if frame_ in (0x73, 0x93):
                self.resetFrameSequence()
                return True
        #  If S -frame.
        if (frame_ & HdlcFrameType.S_FRAME.value) == HdlcFrameType.S_FRAME.value:
            self.receiverFrame = self.increaseReceiverSequence(self.receiverFrame)
            return True
        #  Handle I-frame.
        expected = int()
        if (self.senderFrame & 0x1) == 0:
            expected = GXDLMSSettings.increaseReceiverSequence(GXDLMSSettings.increaseSendSequence(self.receiverFrame))
            if frame_ == expected:
                self.receiverFrame = frame_
                return True
        else:
            expected = self.increaseSendSequence(self.receiverFrame) & 0xFF
            #  If answer for RR.
            if frame_ == expected:
                self.receiverFrame = frame_
                return True
        #  This is for unit tests.
        if self.skipFrameCheck:
            self.receiverFrame = frame_
            return True
        print("Invalid HDLC Frame: " + hex(frame_) + " Expected: " + hex(expected))
        return False

    #
    # Increase receiver sequence.
    #
    # @param value
    # Frame value.
    # Increased receiver frame sequence.
    #
    @classmethod
    def increaseReceiverSequence(cls, value):
        return ((value & 0xFF) + 0x20 | 0x10 | value & 0xE) & 0xFF

    #
    # Increase sender sequence.
    #
    # @param value
    # Frame value.
    # Increased sender frame sequence.
    #
    @classmethod
    def increaseSendSequence(cls, value):
        return ((value & 0xF0 | (value + 0x2) & 0xE) & 0xFF) & 0xFF

    #
    # Generates I-frame.
    # @param first
    # Is this first packet.
    # Generated I-frame
    #
    def getNextSend(self, first):
        if first:
            self.senderFrame = self.increaseReceiverSequence(self.increaseSendSequence(int(self.senderFrame)))
        else:
            self.senderFrame = self.increaseSendSequence(int(self.senderFrame))
        return self.senderFrame & 0xFF

    #
    # Generates Receiver Ready S-frame.
    #
    def getReceiverReady(self):
        self.senderFrame = self.increaseReceiverSequence((self.senderFrame | 1))
        return self.senderFrame & 0xF1

    #
    # Generates Keep Alive S-frame.
    #
    def getKeepAlive(self):
        self.senderFrame = (self.senderFrame | 1)
        return self.senderFrame & 0xF1

    #
    # Gets starting block index in HDLC framing.  Default is One based,
    #      but some
    # meters use Zero based value.  Usually this is not used.
    #
    # Current block index.
    #
    def getStartingPacketIndex(self):
        return self.startingPacketIndex

    #
    # Set starting block index in HDLC framing.  Default is One based,
    #      but some
    # meters use Zero based value.  Usually this is not used.
    #
    # @param value
    # Zero based starting index.
    #
    def setStartingPacketIndex(self, value):
        self.startingPacketIndex = value
        self.resetBlockIndex()

    #
    # Sets current block index.
    #
    # @param value
    # Block index.
    #
    def setBlockIndex(self, value):
        self.blockIndex = value

    #
    # Block number acknowledged in GBT.
    #
    def getBlockNumberAck(self):
        return self.blockNumberAck

    #
    # @param value
    # Block number acknowledged in GBT.
    #
    def setBlockNumberAck(self, value):
        self.blockNumberAck = value

    #
    # Resets block index to default value.
    #
    def resetBlockIndex(self):
        self.blockIndex = self.startingPacketIndex
        self.blockNumberAck = 0

    #
    # Increases block index.
    #
    def increaseBlockIndex(self):
        self.blockIndex += 1

    #
    # Is Logical Name Referencing used.
    #
    def getUseLogicalNameReferencing(self):
        return self.useLogicalNameReferencing

    #
    # @param value
    # Is Logical Name Referencing used.
    #
    def setUseLogicalNameReferencing(self, value):
        if self.useLogicalNameReferencing != value:
            self.useLogicalNameReferencing = value
            self.proposedConformance = GXDLMSSettings.getInitialConformance(self.useLogicalNameReferencing)

    #
    # Invoke ID.
    #
    def getInvokeID(self):
        return self.invokeID

    #
    # @param value
    # update invoke ID.
    #
    def updateInvokeId(self, value):
        if (value & 0x80) != 0:
            self.priority = Priority.HIGH
        else:
            self.priority = Priority.NORMAL
        if (value & 0x40) != 0:
            self.serviceClass = ServiceClass.CONFIRMED
        else:
            self.serviceClass = ServiceClass.UN_CONFIRMED
        self.invokeID = int((value & 0xF))

    #
    # @param value
    # Invoke ID.
    #
    def setInvokeID(self, value):
        if value > 0xF:
            raise ValueError("Invalid InvokeID")
        self.invokeID = int(value)

    #
    # Invoke ID.
    #
    def getLongInvokeID(self):
        return self.longInvokeID

    #
    # @param value
    # Invoke ID.
    #
    def setLongInvokeID(self, value):
        if value > 0xFFFFFFFF:
            raise ValueError("Invalid InvokeID")
        self.longInvokeID = value

    #
    # Source system title.
    #
    def getSourceSystemTitle(self):
        return self.sourceSystemTitle

    #
    # @param value
    # Source system title.
    #
    def setSourceSystemTitle(self, value):
        if not value or len(value) != 8:
            raise ValueError("Invalid client system title.")
        self.sourceSystemTitle = value

    #
    # Long data count.
    #
    def getCount(self):
        return self.count

    #
    # @param value
    # Data count.
    #
    def setCount(self, value):
        if value < 0:
            raise ValueError("Invalid count.")
        self.count = value

    #
    # Long data index.
    #
    def getIndex(self):
        return self.index

    #
    # @param value
    # Long data index
    #
    def setIndex(self, value):
        if value < 0:
            raise ValueError("Invalid Index.")
        self.index = value
