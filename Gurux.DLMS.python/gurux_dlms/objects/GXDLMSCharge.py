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
from .enums import ChargeType
from .GXUnitCharge import GXUnitCharge
from .GXChargeTable import GXChargeTable

#
#  * Online help:
#  * http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSCharge
#
# pylint: disable=too-many-instance-attributes
class GXDLMSCharge(GXDLMSObject, IGXDLMSBase):
    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln="0.0.19.20.0.255", sn=0):
        super(GXDLMSCharge, self).__init__(ObjectType.CHARGE, ln, sn)
        self.totalAmountPaid = 0
        self.priority = 0
        self.unitChargeActivationTime = None
        self.period = 0
        self.chargeConfiguration = 0
        self.lastCollectionTime = None
        self.lastCollectionAmount = 0
        self.totalAmountRemaining = 0
        self.proportion = 0
        self.unitChargeActive = GXUnitCharge()
        self.unitChargePassive = GXUnitCharge()
        self.chargeType = ChargeType.CONSUMPTION_BASED_COLLECTION

    def getValues(self):
        return [self.logicalName,
                self.totalAmountPaid,
                self.chargeType,
                self.priority,
                self.unitChargeActive,
                self.unitChargePassive,
                self.unitChargeActivationTime,
                self.period,
                self.chargeConfiguration,
                self.lastCollectionTime,
                self.lastCollectionAmount,
                self.totalAmountRemaining,
                self.proportion]

    #
    # Returns collection of attributes to read.  If attribute is static
    #      and
    # already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  TotalAmountPaid
        if all_ or self.canRead(2):
            attributes.append(2)
        #  ChargeType
        if all_ or self.canRead(3):
            attributes.append(3)
        #  Priority
        if all_ or self.canRead(4):
            attributes.append(4)
        #  UnitChargeActive
        if all_ or self.canRead(5):
            attributes.append(5)
        #  UnitChargePassive
        if all_ or self.canRead(6):
            attributes.append(6)
        #  UnitChargeActivationTime
        if all_ or self.canRead(7):
            attributes.append(7)
        #  Period
        if all_ or self.canRead(8):
            attributes.append(8)
        #  ChargeConfiguration
        if all_ or self.canRead(9):
            attributes.append(9)
        #  LastCollectionTime
        if all_ or self.canRead(10):
            attributes.append(10)
        #  LastCollectionAmount
        if all_ or self.canRead(11):
            attributes.append(11)
        #  TotalAmountRemaining
        if all_ or self.canRead(12):
            attributes.append(12)
        #  Proportion
        if all_ or self.canRead(13):
            attributes.append(13)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 13

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 5

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
            ret = DataType.STRUCTURE
        elif index == 6:
            ret = DataType.STRUCTURE
        elif index == 7:
            ret = DataType.OCTET_STRING
        elif index == 8:
            ret = DataType.UINT32
        elif index == 9:
            ret = DataType.BITSTRING
        elif index == 10:
            ret = DataType.OCTET_STRING
        elif index == 11:
            ret = DataType.INT32
        elif index == 12:
            ret = DataType.INT32
        elif index == 13:
            ret = DataType.UINT16
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret

    @classmethod
    def getUnitCharge(cls, charge):
        bb = GXByteBuffer()
        bb.setUInt8(DataType.STRUCTURE.value)
        bb.setUInt8(3)
        bb.setUInt8(DataType.STRUCTURE.value)
        bb.setUInt8(2)
        _GXCommon.setData(bb, DataType.INT8, charge.chargePerUnitScaling.commodityScale)
        _GXCommon.setData(bb, DataType.INT8, charge.chargePerUnitScaling.priceScale)
        bb.setUInt8(DataType.STRUCTURE.value)
        bb.setUInt8(3)
        if charge.commodity.target is None:
            _GXCommon.setData(bb, DataType.UINT16, 0)
            bb.setUInt8(DataType.OCTET_STRING.value)
            bb.setUInt8(6)
            bb.setUInt8(0)
            bb.setUInt8(0)
            bb.setUInt8(0)
            bb.setUInt8(0)
            bb.setUInt8(0)
            bb.setUInt8(0)
            _GXCommon.setData(bb, DataType.INT8, 0)
        else:
            _GXCommon.setData(bb, DataType.UINT16, charge.commodity.target.objectType)
            _GXCommon.setData(bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(charge.commodity.target.logicalName))
            _GXCommon.setData(bb, DataType.INT8, charge.commodity.index)
        bb.setUInt8(DataType.ARRAY.value)
        if charge.chargeTables is None:
            bb.setUInt8(0)
        else:
            _GXCommon.setObjectCount(len(charge.chargeTables), bb)
            for it in charge.chargeTables:
                bb.setUInt8(DataType.STRUCTURE.value)
                bb.setUInt8(2)
                _GXCommon.setData(bb, DataType.OCTET_STRING, it.index)
                _GXCommon.setData(bb, DataType.INT16, it.chargePerUnit)
        return bb.array()

    def getValue(self, settings, e):
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            ret = self.totalAmountPaid
        elif e.index == 3:
            ret = self.chargeType.value
        elif e.index == 4:
            ret = self.priority
        elif e.index == 5:
            ret = self.getUnitCharge(self.unitChargeActive)
        elif e.index == 6:
            ret = self.getUnitCharge(self.unitChargePassive)
        elif e.index == 7:
            ret = self.unitChargeActivationTime
        elif e.index == 8:
            ret = self.period
        elif e.index == 9:
            ret = self.chargeConfiguration
        elif e.index == 10:
            ret = self.lastCollectionTime
        elif e.index == 11:
            ret = self.lastCollectionAmount
        elif e.index == 12:
            ret = self.totalAmountRemaining
        elif e.index == 13:
            ret = self.proportion
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    @classmethod
    def setUnitCharge(cls, settings, charge, value):
        tmp = value
        tmp2 = tmp[0]
        charge.chargePerUnitScaling.commodityScale = tmp2[0]
        charge.chargePerUnitScaling.priceScale = tmp2[1]
        tmp2 = tmp[1]
        ot = ObjectType(tmp2[0])
        ln = _GXCommon.toLogicalName(tmp2[1])
        charge.commodity.target = settings.objects.findByLN(ot, ln)
        charge.commodity.index = tmp2[2]
        charge.chargeTables.clear()
        tmp2 = tmp[2]
        for tmp3 in tmp2:
            it = tmp3
            item = GXChargeTable()
            item.index = it[0]
            item.chargePerUnit = it[1]
            charge.chargeTables.append(item)

    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.totalAmountPaid = e.value
        elif e.index == 3:
            self.chargeType = ChargeType(e.value)
        elif e.index == 4:
            self.priority = e.value
        elif e.index == 5:
            self.setUnitCharge(settings, self.unitChargeActive, e.value)
        elif e.index == 6:
            self.setUnitCharge(settings, self.unitChargePassive, e.value)
        elif e.index == 7:
            self.unitChargeActivationTime = _GXCommon.changeType(e.value, DataType.DATETIME)
        elif e.index == 8:
            self.period = e.value
        elif e.index == 9:
            self.chargeConfiguration = str(e.value)
        elif e.index == 10:
            self.lastCollectionTime = _GXCommon.changeType(e.value, DataType.DATETIME)
        elif e.index == 11:
            self.lastCollectionAmount = e.value
        elif e.index == 12:
            self.totalAmountRemaining = e.value
        elif e.index == 13:
            self.proportion = e.value
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @classmethod
    def loadUnitChargeActive(cls, reader, name, charge):
        pass

    def load(self, reader):
        self.totalAmountPaid = reader.readElementContentAsInt("TotalAmountPaid")
        self.chargeType = ChargeType(reader.readElementContentAsInt("ChargeType"))
        self.priority = int(reader.readElementContentAsInt("Priority"))
        self.loadUnitChargeActive(reader, "UnitChargeActive", self.unitChargeActive)
        self.loadUnitChargeActive(reader, "UnitChargePassive", self.unitChargePassive)
        tmp = reader.readElementContentAsString("UnitChargeActivationTime")
        if tmp:
            self.unitChargeActivationTime = GXDateTime(tmp)
        self.period = reader.readElementContentAsInt("Period")
        self.chargeConfiguration = reader.readElementContentAsString("ChargeConfiguration")
        tmp = reader.readElementContentAsString("LastCollectionTime")
        if tmp:
            self.lastCollectionTime = GXDateTime(tmp)
        self.lastCollectionAmount = reader.readElementContentAsInt("LastCollectionAmount")
        self.totalAmountRemaining = reader.readElementContentAsInt("TotalAmountRemaining")
        self.proportion = reader.readElementContentAsInt("Proportion")

    @classmethod
    def saveUnitChargeActive(cls, writer, name, charge):
        pass

    def save(self, writer):
        writer.writeElementString("TotalAmountPaid", self.totalAmountPaid)
        if self.chargeType:
            writer.writeElementString("ChargeType", self.chargeType.value)
        writer.writeElementString("Priority", self.priority)
        self.saveUnitChargeActive(writer, "UnitChargeActive", self.unitChargeActive)
        self.saveUnitChargeActive(writer, "UnitChargePassive", self.unitChargePassive)
        writer.writeElementString("UnitChargeActivationTime", self.unitChargeActivationTime)
        writer.writeElementString("Period", self.period)
        writer.writeElementString("ChargeConfiguration", self.chargeConfiguration)
        writer.writeElementString("LastCollectionTime", self.lastCollectionTime)
        writer.writeElementString("LastCollectionAmount", self.lastCollectionAmount)
        writer.writeElementString("TotalAmountRemaining", self.totalAmountRemaining)
        writer.writeElementString("Proportion", self.proportion)
