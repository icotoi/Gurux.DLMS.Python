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
from ..enums import ObjectType, DataType
from .GXDLMSScheduleEntry import GXDLMSScheduleEntry
from ..GXDateTime import GXDateTime

#
#  * Online help:
#  * http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSSchedule
#
# pylint: disable=too-many-instance-attributes
class GXDLMSSchedule(GXDLMSObject, IGXDLMSBase):
    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln=None, sn=0):
        super(GXDLMSSchedule, self).__init__(ObjectType.SCHEDULE, ln, sn)
        # Specifies the scripts to be executed at given times.
        self.entries = list()

    def getValues(self):
        return [self.logicalName,
                self.entries]

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
        #  Entries
        if all_ or not self.isRead(2):
            attributes.append(2)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):

        return 2

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):

        return 3

    def getDataType(self, index):
        if index == 1:
            return DataType.OCTET_STRING
        if index == 2:
            return DataType.ARRAY
        raise ValueError("getDataType failed. Invalid attribute index.")

    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.entries.clear()
            for it in e.value:
                item = GXDLMSScheduleEntry()
                item.index = it[0]
                item.enable = it[1]
                item.logicalName = _GXCommon.changeType(it[2], DataType.OCTET_STRING)
                item.scriptSelector = it[3]
                item.switchTime = _GXCommon.changeType(it[4], DataType.DATETIME)
                item.validityWindow = it[5]
                item.execWeekdays = it[6]
                item.execSpecDays = it[7]
                item.beginDate = _GXCommon.changeType(it[8], DataType.DATETIME)
                item.endDate = _GXCommon.changeType(it[9], DataType.DATETIME)
                self.entries.append(item)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        self.entries.clear()
        if reader.isStartElement("Entries", True):
            while reader.isStartElement("Item", True):
                it = GXDLMSScheduleEntry()
                it.index = reader.readElementContentAsInt("Index")
                it.enable = reader.readElementContentAsInt("Enable") != 0
                it.logicalName = reader.readElementContentAsString("LogicalName")
                it.scriptSelector = reader.readElementContentAsInt("ScriptSelector")
                it.switchTime = reader.readElementContentAsObject("SwitchTime", GXDateTime())
                it.validityWindow = reader.readElementContentAsInt("ValidityWindow")
                it.execWeekdays = reader.readElementContentAsString("ExecWeekdays")
                it.execSpecDays = reader.readElementContentAsString("ExecSpecDays")
                it.beginDate = reader.readElementContentAsObject("BeginDate", GXDateTime())
                it.endDate = reader.readElementContentAsObject("EndDate", GXDateTime())
                self.entries.append(it)
            reader.readEndElement("Entries")

    def save(self, writer):
        if self.entries:
            writer.writeStartElement("Entries")
            for it in self.entries:
                writer.writeStartElement("Item")
                writer.writeElementString("Index", it.index)
                writer.writeElementString("Enable", it.enable)
                writer.writeElementString("LogicalName", it.logicalName)
                writer.writeElementString("ScriptSelector", it.scriptSelector)
                writer.writeElementObject("SwitchTime", it.switchTime)
                writer.writeElementString("ValidityWindow", it.validityWindow)
                writer.writeElementString("ExecWeekdays", it.execWeekdays)
                writer.writeElementString("ExecSpecDays", it.execSpecDays)
                writer.writeElementObject("BeginDate", it.beginDate)
                writer.writeElementObject("EndDate", it.endDate)
                writer.writeEndElement()
            writer.writeEndElement()
