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
import xml.etree.cElementTree as ET
from collections import deque
from ..enums import DataType
from ..GXByteBuffer import GXByteBuffer
from ..GXDateTime import GXDateTime
from ..GXDate import GXDate
from ..GXTime import GXTime
from ..GXDLMSConverter import GXDLMSConverter

class GXXmlReader():
    """Read serialized COSEM object from the file."""

    def __init__(self, filename, objects):
        """
        Constructor.
        filename: File name.
        """
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.iter = self.tree.iter()
        self.currentElement = None
        self.objects = objects
        dd = deque(self.tree.iter(), maxlen=1)
        self.last_element = dd.pop()

    def getNext(self):
        if self.isEOF():
            return None
        self.currentElement = next(self.iter)
        return self.currentElement

    def isEOF(self):
        return self.currentElement == self.last_element

    @classmethod
    def read(cls):
        return True

    def readEndElement(self, name):
        if name == self.name():
            self.getNext()

    def name(self):
        return self.currentElement.tag

    def isStartElement(self, name=None, getNext=False):
        if name is None:
            ret = isinstance(self.currentElement, ET.Element)
        else:
            ret = isinstance(self.currentElement, ET.Element) and self.currentElement.tag == name
        if ret and getNext:
            self.getNext()
        return ret

    def getAttribute(self, index):
        for it in self.currentElement.attrib:
            if index == 0:
                return self.currentElement.attrib[it]
            index -= 1
        return None

    def readElementContentAsInt(self, name, defaultValue=0):
        if name == self.name():
            str_ = self.currentElement.text
            ret = int(str_)
            self.getNext()
            return ret
        return defaultValue

    def readElementContentAsLong(self, name, defaultValue=0):
        return self.readElementContentAsInt(name, defaultValue)

    def readElementContentAsULong(self, name, defaultValue):
        return self.readElementContentAsInt(name, defaultValue)

    def readElementContentAsDouble(self, name, defaultValue=0):
        if name == self.name():
            str_ = self.currentElement.text
            ret = float(str_)
            self.getNext()
            return ret
        return defaultValue

    def readArray(self):
        list_ = list()
        while self.isStartElement("Item", False):
            list_.append(self.readElementContentAsObject("Item", None))
        return list_

    def readElementContentAsObject(self, name, defaultValue):
        if name == self.name():
            ret = None
            str_ = self.getAttribute(0)
            tp = DataType(int(str_))
            if tp == DataType.ARRAY:
                self.getNext()
                ret = self.readArray()
                self.readEndElement(name)
            else:
                str_ = self.currentElement.text
                if tp == DataType.OCTET_STRING:
                    ret = GXByteBuffer.hexToBytes(str_)
                elif tp == DataType.DATETIME:
                    ret = GXDateTime(str_)
                elif tp == DataType.DATE:
                    ret = GXDate(str_)
                elif tp == DataType.TIME:
                    ret = GXTime(str_)
                else:
                    ret = GXDLMSConverter.changeType(str_, tp)
                self.getNext()
            return ret
        return defaultValue

    def readElementContentAsString(self, name, defaultValue=None):
        if name == self.currentElement.tag:
            str_ = self.currentElement.text
            self.getNext()
            return str_
        return defaultValue
