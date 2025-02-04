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
from ..internal._GXCommon import _GXCommon
from ..GXDateTime import GXDateTime
from ..enums import ObjectType, DataType, Unit

#
#  * Online help:
#  * http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSProfileGeneric
#
# pylint: disable=too-many-instance-attributes
class GXDLMSExtendedRegister(GXDLMSObject, IGXDLMSBase):
    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    def __init__(self, ln=None, sn=0):
        super(GXDLMSExtendedRegister, self).__init__(ObjectType.EXTENDED_REGISTER, ln, sn)
        self.value = None
        self.scaler = 1
        self.unit = Unit.NONE
        self.status = None
        self.captureTime = None

    def getUIDataType(self, index):
        if index == 5:
            return DataType.DATETIME
        return super(GXDLMSExtendedRegister, self).getUIDataType(index)

    def getValues(self):
        return [self.logicalName,
                self.value,
                [self.scaler, self.unit],
                self.status,
                self.captureTime]

    #
    #      Returns collection of attributes to read.  If attribute is static
    #      and
    #      already read or device is returned HW error it is not returned.
    #
    def getAttributeIndexToRead(self, all_):
        attributes = list()
        #  LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        #  ScalerUnit
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  Value
        if all_ or self.canRead(2):
            attributes.append(2)
        #  Status
        if all_ or self.canRead(4):
            attributes.append(4)
        #  CaptureTime
        if all_ or self.canRead(5):
            attributes.append(5)
        return attributes

    #
    #      Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 5

    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = super(GXDLMSExtendedRegister, self).getDataType(index)
        elif index == 3:
            ret = DataType.ARRAY
        elif index == 4:
            ret = super(GXDLMSExtendedRegister, self).getDataType(index)
        elif index == 5:
            ret = DataType.OCTET_STRING
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    #      Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 4:
            return self.status
        if e.index == 5:
            return self.captureTime
        return super(GXDLMSExtendedRegister, self).getValue(settings, e)

    #
    #      Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 4:
            self.status = e.value
        elif e.index == 5:
            if e.value is None:
                self.captureTime = GXDateTime()
            else:
                if isinstance(e.value, bytearray):
                    self.captureTime = _GXCommon.changeType(e.value, DataType.DATETIME)
                else:
                    self.captureTime = e.value
        else:
            super(GXDLMSExtendedRegister, self).setValue(settings, e)

    def load(self, reader):
        self.unit = Unit(reader.readElementContentAsInt("Unit", 0))
        self.scaler = reader.readElementContentAsDouble("Scaler", 1)
        self.value = reader.readElementContentAsObject("Value", None)
        self.status = reader.readElementContentAsObject("Status", None)
        self.captureTime = reader.readElementContentAsObject("CaptureTime", None)

    def save(self, writer):
        writer.writeElementString("Unit", self.unit.value)
        writer.writeElementString("Scaler", self.scaler, 1)
        writer.writeElementObject("Value", self.value)
        writer.writeElementObject("Status", self.status)
        writer.writeElementObject("CaptureTime", self.captureTime)
