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
from ..enums import ErrorCode, DateTimeSkips
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..GXTime import GXTime
from ..GXDate import GXDate
from ..enums import ObjectType, DataType
from .enums import SingleActionScheduleType
from .GXDLMSScriptTable import GXDLMSScriptTable

# pylint: disable=too-many-instance-attributes
class GXDLMSActionSchedule(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
    http://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSActionSchedule
    """

    #
    # Constructor.
    #
    # @param ln
    # Logical Name of the object.
    # @param sn
    # Short Name of the object.
    #
    def __init__(self, ln="0.0.15.0.0.255", sn=0):
        super(GXDLMSActionSchedule, self).__init__(ObjectType.ACTION_SCHEDULE, ln, sn)
        self.type_ = SingleActionScheduleType.SingleActionScheduleType1
        # Script to execute.
        self.target = None
        self.executedScriptLogicalName = None
        self.executedScriptSelector = 0
        self.executionTime = list()

    def getValues(self):
        return [self.logicalName,
                [self.executedScriptLogicalName, self.executedScriptSelector],
                self.type_,
                self.executionTime]

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
        #  ExecutedScriptLogicalName is static and read only once.
        if all_ or not self.isRead(2):
            attributes.append(2)
        #  Type is static and read only once.
        if all_ or not self.isRead(3):
            attributes.append(3)
        #  ExecutionTime is static and read only once.
        if all_ or not self.isRead(4):
            attributes.append(4)
        return attributes

    #
    # Returns amount of attributes.
    #
    def getAttributeCount(self):
        return 4

    #
    # Returns amount of methods.
    #
    def getMethodCount(self):
        return 0

    def getDataType(self, index):
        if index == 1:
            ret = DataType.OCTET_STRING
        elif index == 2:
            ret = DataType.ARRAY
        elif index == 3:
            return DataType.ENUM
        elif index == 4:
            return DataType.ARRAY
        else:
            raise ValueError("getDataType failed. Invalid attribute index.")
        return ret
    #
    # Returns value of given attribute.
    #
    def getValue(self, settings, e):
        if e.index == 1:
            return _GXCommon.logicalNameToBytes(self.logicalName)
        if e.index == 2:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.STRUCTURE.value)
            bb.setUInt8(2)
            _GXCommon.setData(bb, DataType.OCTET_STRING, _GXCommon.logicalNameToBytes(self.executedScriptLogicalName))
            _GXCommon.setData(bb, DataType.UINT16, int(self.executedScriptSelector))
            return bb.array()
        if e.index == 3:
            return int(self.type_.value)
        if e.index == 4:
            bb = GXByteBuffer()
            bb.setUInt8(DataType.ARRAY.value)
            if not self.executionTime:
                _GXCommon.setObjectCount(0, bb)
            else:
                _GXCommon.setObjectCount(len(self.executionTime), bb)
                for it in self.executionTime:
                    bb.setUInt8(DataType.STRUCTURE.value)
                    #  Count
                    bb.setUInt8(2)
                    #  Time
                    _GXCommon.setData(bb, DataType.OCTET_STRING, GXTime(it))
                    #  Date
                    _GXCommon.setData(bb, DataType.OCTET_STRING, GXDate(it))
            return bb.array()
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    #
    # Set value of given attribute.
    #
    def setValue(self, settings, e):
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            self.executedScriptLogicalName = _GXCommon.toLogicalName(e.value[0])
            self.executedScriptSelector = e.value[1]
        elif e.index == 3:
            self.type_ = SingleActionScheduleType(e.value)
        elif e.index == 4:
            self.executionTime.clear()
            if e.value:
                for it in e.value:
                    time = _GXCommon.changeType(it[0], DataType.TIME)
                    date = _GXCommon.changeType(it[1], DataType.DATE)
                    tmp = GXDateTime(date.value)
                    tmp.value = tmp.value.replace(hour=time.value.hour, minute=time.value.minute, second=time.value.second)
                    tmp.skip = (date.skip & (DateTimeSkips.YEAR | DateTimeSkips.MONTH | DateTimeSkips.DAY | DateTimeSkips.DAY_OF_WEEK))
                    tmp.skip |= (time.skip & (DateTimeSkips.HOUR | DateTimeSkips.MINUTE | DateTimeSkips.SECOND | DateTimeSkips.MILLISECOND))
                    self.executionTime.append(tmp)
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    def load(self, reader):
        ot = ObjectType(reader.readElementContentAsInt("ObjectType"))
        ln = reader.readElementContentAsString("LN")
        if ot != ObjectType.NONE and ln:
            self.target = reader.objects.findByLN(ot, ln)
            #  if object is not load yet.
            if self.target:
                self.target = GXDLMSScriptTable(ln)
        self.executedScriptSelector = reader.readElementContentAsInt("ExecutedScriptSelector")
        self.type_ = SingleActionScheduleType(reader.readElementContentAsInt("Type"))
        self.executionTime.clear()
        if reader.isStartElement("ExecutionTime", True):
            while reader.isStartElement("Time", False):
                it = GXDateTime(reader.readElementContentAsString("Time"))
                self.executionTime.append(it)
            reader.readEndElement("ExecutionTime")

    def save(self, writer):
        if self.target:
            writer.writeElementString("ObjectType", self.target.objectType.value)
            writer.writeElementString("LN", self.target.logicalName)
        writer.writeElementString("ExecutedScriptSelector", self.executedScriptSelector)
        writer.writeElementString("Type", self.type_.value)
        if self.executionTime:
            writer.writeStartElement("ExecutionTime")
            for it in self.executionTime:
                writer.writeElementString("Time", it.toFormatString())
            writer.writeEndElement()

    def postLoad(self, reader):
        #  Upload target after load.
        if self.target:
            t = reader.objects.findByLN(ObjectType.SCRIPT_TABLE, self.target.logicalName)
            if self.target != t:
                self.target = t
