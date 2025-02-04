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
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType
from .enums import CreditConfiguration, CreditType, CreditStatus

#
#  * Online help:
#  * http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSCredit
#
# pylint: disable=too-many-instance-attributes
class GXDLMSCredit(GXDLMSObject, IGXDLMSBase):
    #
    # Constructor.
    #
    # @param ln
    #            Logical Name of the object.
    # @param sn
    #            Short Name of the object.
    #
    def __init__(self, ln="0.0.19.10.0.255", sn=0):
        super(GXDLMSCredit, self).__init__(ObjectType.CREDIT, ln, sn)
        self.creditConfiguration = CreditConfiguration.TOKENS
        self.type_ = CreditType.TOKEN
        self.status = CreditStatus.ENABLED
        self.currentCreditAmount = 0
        self.priority = 0
        self.warningThreshold = 0
        self.limit = 0
        self.creditConfiguration = None
        self.presetCreditAmount = 0
        self.creditAvailableThreshold = 0
        self.period = None

    def getValues(self):
        return [self.logicalName,
                self.currentCreditAmount,
                self.type_,
                self.priority,
                self.warningThreshold,
                self.limit,
                self.creditConfiguration,
                self.status,
                self.presetCreditAmount,
                self.creditAvailableThreshold,
                self.period]

    #
    # Returns collection of attributes to read.  If attribute is static and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  CurrentCreditAmount
        if all_ or self.canRead(2):
            attributes.append(2)
        #  Type
        if all_ or self.canRead(3):
            attributes.append(3)
        #  Priority
        if all_ or self.canRead(4):
            attributes.append(4)
        #  WarningThreshold
        if all_ or self.canRead(5):
            attributes.append(5)
        #  Limit
        if all_ or self.canRead(6):
            attributes.append(6)
        #  creditConfiguration
        if all_ or self.canRead(7):
            attributes.append(7)
        #  Status
        if all_ or self.canRead(8):
            attributes.append(8)
        #  PresetCreditAmount
        if all_ or self.canRead(9):
            attributes.append(9)
        #  CreditAvailableThreshold
        if all_ or self.canRead(10):
            attributes.append(10)
        #  Period
        if all_ or self.canRead(11):
            attributes.append(11)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):

        return 11

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):

        return 3

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.INT32
        elif index == 3:
            ret = DataType.ENUM
        elif index == 4:
            ret = DataType.UINT8
        elif index == 5:
            ret = DataType.INT32
        elif index == 6:
            ret = DataType.INT32
        elif index == 7:
            ret = DataType.BITSTRING
        elif index == 8:
            ret = DataType.ENUM
        elif index == 9:
            ret = DataType.INT32
        elif index == 10:
            ret = DataType.INT32
        elif index == 11:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.currentCreditAmount
        elif e.index == 3:
            ret = self.type_.value
        elif e.index == 4:
            ret = self.priority
        elif e.index == 5:
            ret = self.warningThreshold
        elif e.index == 6:
            ret = self.limit
        elif e.index == 7:
            ret = self.creditConfiguration
        elif e.index == 8:
            ret = self.status.value
        elif e.index == 9:
            ret = self.presetCreditAmount
        elif e.index == 10:
            ret = self.creditAvailableThreshold
        elif e.index == 11:
            ret = self.period
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.currentCreditAmount = e.value
        elif e.index == 3:
            self.type_ = CreditType(e.value)
        elif e.index == 4:
            self.priority = e.value
        elif e.index == 5:
            self.warningThreshold = e.value
        elif e.index == 6:
            self.limit = e.value
        elif e.index == 7:
            bb = GXByteBuffer()
            _GXCommon.setBitString(bb, e.value, False)
            self.creditConfiguration = CreditConfiguration(bb.getUInt8(0))
        elif e.index == 8:
            self.status = CreditStatus(e.value)
        elif e.index == 9:
            self.presetCreditAmount = e.value
        elif e.index == 10:
            self.creditAvailableThreshold = e.value
        elif e.index == 11:
            if e.value is None:
                self.period = GXDateTime()
            else:
                tmp = None
                if isinstance(e.value, bytearray):
                    tmp = _GXCommon.changeType(e.value, DataType.DATETIME)
                else:
                    tmp = e.value
                self.period = tmp
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.currentCreditAmount = reader.readElementContentAsInt("CurrentCreditAmount")
        self.type_ = CreditType(reader.readElementContentAsInt("Type"))
        self.priority = int(reader.readElementContentAsInt("Priority"))
        self.warningThreshold = reader.readElementContentAsInt("WarningThreshold")
        self.limit = reader.readElementContentAsInt("Limit")
        self.creditConfiguration = CreditConfiguration(reader.readElementContentAsInt("CreditConfiguration"))
        self.status = CreditStatus(reader.readElementContentAsInt("Status"))
        self.presetCreditAmount = reader.readElementContentAsInt("PresetCreditAmount")
        self.creditAvailableThreshold = reader.readElementContentAsInt("CreditAvailableThreshold")
        str_ = reader.readElementContentAsString("Period")
        if str_:
            self.period = GXDateTime(str_)

    def save(self, writer):
        writer.writeElementString("CurrentCreditAmount", self.currentCreditAmount)
        if self.type_:
            writer.writeElementString("Type", self.type_.value)
        writer.writeElementString("Priority", self.priority)
        writer.writeElementString("WarningThreshold", self.warningThreshold)
        writer.writeElementString("Limit", self.limit)
        writer.writeElementString("CreditConfiguration", self.creditConfiguration)
        writer.writeElementString("Status", self.status)
        writer.writeElementString("PresetCreditAmount", self.presetCreditAmount)
        writer.writeElementString("CreditAvailableThreshold", self.creditAvailableThreshold)
        writer.writeElementString("Period", self.period)
