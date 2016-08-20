#####################################################################
# functions.py
#
# (c) Copyright 2013-2015, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
"""Wrappers for SECS stream and functions"""

from collections import OrderedDict

from functionbase import SecsStreamFunction
from dataitems import *


class SecsS00F00(SecsStreamFunction):
    """Secs stream and function class for stream 00, function 00 - hsms communication

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS00F00()
        S0F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 0
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS01F00(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 00 - abort transaction stream 1

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F00()
        S1F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS01F01(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 01 - are you online - request

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F01()
        S1F1 W

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 1

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS01F02(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 02 - on line data

    .. caution::

        This Stream/function has different structures depending on the source.
        If it is sent from the eqipment side it has the structure below, if it is sent from the host it is an empty list.
        Be sure to fill the array accordingly.

    **Structure E->H**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F02(['secsgem', '0.0.3']) # E->H
        S1F2
          <L [2]
            <A "secsgem">
            <A "0.0.3">
          >
        >>> secsgem.SecsS01F02() #H->E
        S1F2
          <L>

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 2

    _formatDescriptor = SecsVarArray(SecsVarString(20))

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS01F03(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 03 - selected equipment status - request

    **Data Items**

    - :class:`SVID <secsgem.secs.dataitems.SVID>`

    **Structure**::

        [
            SVID: A/I*/U*
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F03([1, "1337", 12])
        S1F3 W
          <L [3]
            <I1 1 >
            <A "6">
            <I1 12 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 3

    _formatDescriptor = SecsVarArray(SVID())

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS01F04(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 04 - selected equipment status - data

    **Data Items**

    - :class:`SV <secsgem.secs.dataitems.SV>`

    **Structure**::

        [
            SV: any
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F04([secsgem.SecsVarU1(value=1), "text", secsgem.SecsVarU4(value=1337)])
        S1F4
          <L [3]
            <U1 1 >
            <A "text">
            <U4 1337 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 4

    _formatDescriptor = SecsVarArray(SV())

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS01F11(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 11 - status variable namelist - request

    **Data Items**

    - :class:`SVID <secsgem.secs.dataitems.SVID>`

    **Structure**::

        [
            SVID: A/I*/U*
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F11([1, 1337])
        S1F11 W
          <L [2]
            <I1 1 >
            <I2 1337 >
          > .

    An empty list will return all available status variables.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 11

    _formatDescriptor = SecsVarArray(SVID())

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS01F12(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 12 - status variable namelist - reply

    **Data Items**

    - :class:`SVID <secsgem.secs.dataitems.SVID>`
    - :class:`SVNAME <secsgem.secs.dataitems.SVNAME>`
    - :class:`UNITS <secsgem.secs.dataitems.UNITS>`

    **Structure**::

        [
            {
                SVID: A/I*/U*
                SVNAME: A[n]
                UNITS: A[n]
            }
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F12([{"SVID": 1, "SVNAME": "SV1", "UNITS": "mm"}, {"SVID": 1337, "SVNAME": "SV2", "UNITS": ""}])
        S1F12
          <L [2]
            <L [3]
              <I1 1 >
              <A "SV1">
              <A "mm">
            >
            <L [3]
              <I2 1337 >
              <A "SV2">
              <A>
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 12

    _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
        ("SVID", SVID()),
        ("SVNAME", SVNAME()),
        ("UNITS", UNITS()),
    )), 3))

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS01F13(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 13 - establish communication - request

    .. caution::

        This Stream/function has different structures depending on the source.
        If it is sent from the eqipment side it has the structure below, if it is sent from the host it is an empty list.
        Be sure to fill the array accordingly.

    **Structure E->H**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F13(['secsgem', '0.0.3']) # E->H
        S1F13 W
          <L [2]
            <A "secsgem">
            <A "0.0.3">
          >
        >>> secsgem.SecsS01F13() #H->E
        S1F13 W
          <L>

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 1
    _function = 13

    _formatDescriptor = SecsVarArray(SecsVarString(20))

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS01F14(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 14 - establish communication - acknowledge

    .. caution::

        This Stream/function has different structures depending on the source.
        See structure definition below for details.
        Be sure to fill the array accordingly.

    **Data Items**

    - :class:`COMMACK <secsgem.secs.dataitems.COMMACK>`

    **Structure E->H**::

        {
            COMMACK: B[1]
            DATA: {
                MDLN: A[20]
                SOFTREV: A[20]
            }
        }

    **Structure H->E**::

        {
            COMMACK: B[1]
            DATA: []
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F14({"COMMACK": secsgem.COMMACK.ACCEPTED, "DATA": ["secsgem", "0.0.3"]})
        S1F14
          <L [2]
            <B 0x0>
            <L [2]
              <A "secsgem">
              <A "0.0.3">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 1
    _function = 14

    _formatDescriptor = SecsVarList(OrderedDict((
        ("COMMACK", COMMACK()),
        ("DATA", SecsVarArray(SecsVarString(20)))
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS01F15(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 15 - request offline

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F15()
        S1F15 W

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 15

    _formatDescriptor = None

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS01F16(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 16 - offline acknowledge

    **Data Items**

    - :class:`OFLACK <secsgem.secs.dataitems.OFLACK>`

    **Structure**::

        OFLACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F16(secsgem.OFLACK.ACK)
        S1F16
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 1
    _function = 16

    _formatDescriptor = OFLACK()

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS01F17(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 17 - request offline

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F17()
        S1F17 W

    :param value: function has no parameters
    :type value: None
    """
    _stream = 1
    _function = 17

    _formatDescriptor = None

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS01F18(SecsStreamFunction):
    """Secs stream and function class for stream 01, function 18 - online acknowledge

    **Data Items**

    - :class:`ONLACK <secsgem.secs.dataitems.ONLACK>`

    **Structure**::

        ONLACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS01F18(secsgem.ONLACK.ALREADYON)
        S1F18
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 1
    _function = 18

    _formatDescriptor = ONLACK()

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS02F00(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 00 - abort transaction stream 2

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F00()
        S2F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 2
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS02F13(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 13 - equipment constant - request

    **Data Items**

    - :class:`ECID <secsgem.secs.dataitems.ECID>`

    **Structure**::

        [
            ECID: A/I*/U*
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F13([1, 1337])
        S2F13 W
          <L [2]
            <I1 1 >
            <I2 1337 >
          > .

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 13

    _formatDescriptor = SecsVarArray(ECID())

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS02F14(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 14 - equipment constant - data

    **Data Items**

    - :class:`ECV <secsgem.secs.dataitems.ECV>`

    **Structure**::

        [
            ECV: any
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F14([secsgem.SecsVarU1(value=1), "text"])
        S2F14
          <L [2]
            <U1 1 >
            <A "text">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 14

    _formatDescriptor = SecsVarArray(ECV())

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS02F15(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 15 - new equipment constant - send

    **Data Items**

    - :class:`ECID <secsgem.secs.dataitems.ECID>`
    - :class:`ECV <secsgem.secs.dataitems.ECV>`

    **Structure**::

        [
            {
                ECID: A/I*/U*
                ECV: any
            }
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F15([{"ECID": 1, "ECV": secsgem.SecsVarU4(value=10)}, {"ECID": "1337", "ECV": "text"}])
        S2F15 W
          <L [2]
            <L [2]
              <I1 1 >
              <U4 10 >
            >
            <L [2]
              <A "1337">
              <A "text">
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 15

    _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
        ("ECID", ECID()),
        ("ECV", ECV()),
    )), 2))

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS02F16(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 16 - new equipment constant - acknowledge

    **Data Items**

    - :class:`EAC <secsgem.secs.dataitems.EAC>`

    **Structure**::

        EAC: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F16(secsgem.EAC.BUSY)
        S2F16
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 16

    _formatDescriptor = EAC()

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS02F17(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 17 - date and time - request

    **Structure**::

        Header only

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F17()
        S2F17 W .

    :param value: function has no parameters
    :type value: None
    """
    _stream = 2
    _function = 17

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS02F18(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 18 - date and time - data

    **Data Items**

    - :class:`TIME <secsgem.secs.dataitems.TIME>`

    **Structure**::

        TIME: A[32]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F18("160816205942")
        S2F18
          <A "160816205942"> .

    :param value: parameters for this function (see example)
    :type value: ASCII string
    """
    _stream = 2
    _function = 18

    _formatDescriptor = TIME()

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False
    
    
class SecsS02F29(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 29 - equipment constant namelist - request

    **Data Items**

    - :class:`ECID <secsgem.secs.dataitems.ECID>`

    **Structure**::

        [
            ECID: A/I*/U*
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F29([1, 1337])
        S2F29 W
          <L [2]
            <I1 1 >
            <I2 1337 >
          > .

    An empty list will return all available equipment constants.

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 29

    _formatDescriptor = SecsVarArray(ECID())

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS02F30(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 30 - equipment constant namelist

    **Data Items**

    - :class:`ECID <secsgem.secs.dataitems.ECID>`
    - :class:`ECNAME <secsgem.secs.dataitems.ECNAME>`
    - :class:`ECMIN <secsgem.secs.dataitems.ECMIN>`
    - :class:`ECMAX <secsgem.secs.dataitems.ECMAX>`
    - :class:`ECDEF <secsgem.secs.dataitems.ECDEF>`
    - :class:`UNITS <secsgem.secs.dataitems.UNITS>`

    **Structure**::

        [
            {
                ECID: A/I*/U*
                ECNAME: A
                ECMIN: any
                ECMAX: any
                ECDEF: any
                UNITS: A
            }
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F30([{"ECID": 1, "ECNAME": "EC1", "ECMIN": secsgem.SecsVarU1(value=0), "ECMAX": secsgem.SecsVarU1(value=100), "ECDEF": secsgem.SecsVarU1(value=50), "UNITS": "mm"}, {"ECID": 1337, "ECNAME": "EC2", "ECMIN": "", "ECMAX": "", "ECDEF": "", "UNITS": ""}])
        S2F30
          <L [2]
            <L [6]
              <I1 1 >
              <A "EC1">
              <U1 0 >
              <U1 100 >
              <U1 50 >
              <A "mm">
            >
            <L [6]
              <I2 1337 >
              <A "EC2">
              <A>
              <A>
              <A>
              <A>
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 30

    _formatDescriptor = SecsVarArray(SecsVarList(OrderedDict((
        ("ECID", ECID()),
        ("ECNAME", ECNAME()),
        ("ECMIN", ECMIN()),
        ("ECMAX", ECMAX()),
        ("ECDEF", ECDEF()),
        ("UNITS", UNITS()),
    )), 6))

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS02F33(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 33 - define report

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`
    - :class:`RPTID <secsgem.secs.dataitems.RPTID>`
    - :class:`VID <secsgem.secs.dataitems.VID>`

    **Structure**::

        {
            DATAID: A/I*/U*
            DATA: [
                {
                    RPTID: A/I*/U*
                    RPT: [
                        VID: A/I*/U*
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F33({"DATAID": 1, "DATA": [{"RPTID": 1000, "VID": [12, 1337]}, {"RPTID": 1001, "VID": [1, 2355]}]})
        S2F33 W
          <L [2]
            <I1 1 >
            <L [2]
              <L [2]
                <I2 1000 >
                <L [2]
                  <I1 12 >
                  <I2 1337 >
                >
              >
              <L [2]
                <I2 1001 >
                <L [2]
                  <I1 1 >
                  <I2 2355 >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 33

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", DATAID()),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RPTID", RPTID()),
                ("VID", SecsVarArray(VID())),
            )), 2)
        )),
    )), 2)

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS02F34(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 34 - define report - acknowledge

    **Data Items**

    - :class:`DRACK <secsgem.secs.dataitems.DRACK>`

    **Structure**::

        DRACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F34(secsgem.DRACK.INVALIDFORMAT)
        S2F34
          <B 0x2> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 34

    _formatDescriptor = DRACK()

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS02F35(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 35 - link event report

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`
    - :class:`CEID <secsgem.secs.dataitems.CEID>`
    - :class:`RPTID <secsgem.secs.dataitems.RPTID>`

    **Structure**::

        {
            DATAID: A/I*/U*
            DATA: [
                {
                    CEID: A/I*/U*
                    RPTID: [
                        ID: A/I*/U*
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F35({"DATAID": 1, "DATA": [{"CEID": 1337, "RPTID": [1000, 1001]}]})
        S2F35 W
          <L [2]
            <I1 1 >
            <L [1]
              <L [2]
                <I2 1337 >
                <L [2]
                  <I2 1000 >
                  <I2 1001 >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 35

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", DATAID()),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("CEID", CEID()),
                ("RPTID", SecsVarArray(
                    RPTID()
                )),
            )), 2)
        )),
    )), 2)

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS02F36(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 36 - link event report - acknowledge

    **Data Items**

    - :class:`LRACK <secsgem.secs.dataitems.LRACK>`

    **Structure**::

        LRACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F36(secsgem.LRACK.CEIDUNKNOWN)
        S2F36
          <B 0x4> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 36

    _formatDescriptor = LRACK()

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS02F37(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 37 - en-/disable event report

    **Data Items**

    - :class:`CEED <secsgem.secs.dataitems.CEED>`
    - :class:`CEID <secsgem.secs.dataitems.CEID>`

    **Structure**::

        {
            CEED: BOOL[1]
            CEID: [
                ID: A/I*/U*
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F37({"CEED": True, "CEID": [1337]})
        S2F37 W
          <L [2]
            <BOOLEAN True >
            <L [1]
              <I2 1337 >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 37

    _formatDescriptor = SecsVarList(OrderedDict((
        ("CEED", CEED()),
        ("CEID", SecsVarArray(CEID())),
    )), 2)

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS02F38(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 38 - en-/disable event report - acknowledge

    **Data Items**

    - :class:`ERACK <secsgem.secs.dataitems.ERACK>`

    **Structure**::

        ERACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F38(secsgem.ERACK.CEIDUNKNOWN)
        S2F38
          <B 0x1> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 2
    _function = 38

    _formatDescriptor = ERACK()

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS02F41(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 41 - host command - send

    **Data Items**

    - :class:`RCMD <secsgem.secs.dataitems.RCMD>`
    - :class:`CPNAME <secsgem.secs.dataitems.CPNAME>`
    - :class:`CPVAL <secsgem.secs.dataitems.CPVAL>`

    **Structure**::

        {
            RCMD: A/U1/I1
            PARAMS: [
                {
                    CPNAME: A/I*/U*
                    CPVAL: B/BOOL/A/I*/U*
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F41({"RCMD": "COMMAND", "PARAMS": [{"CPNAME": "PARAM1", "CPVAL": "VAL1"}, {"CPNAME": "PARAM2", "CPVAL": "VAL2"}]})
        S2F41 W
          <L [2]
            <A "COMMAND">
            <L [2]
              <L [2]
                <A "PARAM1">
                <A "VAL1">
              >
              <L [2]
                <A "PARAM2">
                <A "VAL2">
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 41

    _formatDescriptor = SecsVarList(OrderedDict((
        ("RCMD", RCMD()),
        ("PARAMS", SecsVarArray(
            SecsVarList(OrderedDict((
                ("CPNAME", CPNAME()),
                ("CPVAL", CPVAL()),
            )), 2)
        )),
    )), 2)

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS02F42(SecsStreamFunction):
    """Secs stream and function class for stream 02, function 42 - host command - acknowledge

    **Data Items**

    - :class:`HCACK <secsgem.secs.dataitems.HCACK>`
    - :class:`CPNAME <secsgem.secs.dataitems.CPNAME>`
    - :class:`CPACK <secsgem.secs.dataitems.CPACK>`

    **Structure**::

        {
            HCACK: B[1]
            PARAMS: [
                {
                    CPNAME: A/I*/U*
                    CPACK: B[1]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS02F42({"HCACK": secsgem.HCACK.INVALIDCOMMAND, "PARAMS": [{"CPNAME": "PARAM1", "CPACK": secsgem.CPACK.CPVALILLEGALVALUE}, {"CPNAME": "PARAM2", "CPACK": secsgem.CPACK.CPVALILLEGALFORMAT}]})
        S2F42
          <L [2]
            <B 0x1>
            <L [2]
              <L [2]
                <A "PARAM1">
                <B 0x2>
              >
              <L [2]
                <A "PARAM2">
                <B 0x3>
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 2
    _function = 42

    _formatDescriptor = SecsVarList(OrderedDict((
        ("HCACK", HCACK()),
        ("PARAMS", SecsVarArray(
            SecsVarList(OrderedDict((
                ("CPNAME", CPNAME()),
                ("CPACK", CPACK()),
            )), 2)
        )),
    )), 2)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS05F00(SecsStreamFunction):
    """Secs stream and function class for stream 05, function 00 - abort transaction stream 5

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS05F00()
        S5F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 5
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS05F01(SecsStreamFunction):
    """Secs stream and function class for stream 05, function 01 - alarm report - send

    **Data Items**

    - :class:`ALCD <secsgem.secs.dataitems.ALCD>`
    - :class:`ALID <secsgem.secs.dataitems.ALID>`
    - :class:`ALTX <secsgem.secs.dataitems.ALTX>`

    **Structure**::

        {
            ALCD: B[1]
            ALID: U*/I*
            ALTX: A[120]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS05F01({"ALCD": secsgem.ALCD.PERSONALSAFETY | secsgem.ALCD.ALARMSET, "ALID": 100, "ALTX": "text"})
        S5F1
          <L [3]
            <B 0x81>
            <I1 100 >
            <A "text">
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 5
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("ALCD", ALCD()),
        ("ALID", ALID()),
        ("ALTX", ALTX()),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS05F02(SecsStreamFunction):
    """Secs stream and function class for stream 05, function 02 - alarm report - acknowledge

    **Data Items**

    - :class:`ACKC5 <secsgem.secs.dataitems.ACKC5>`

    **Structure**::

        ACKC5: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS05F02(secsgem.ACKC5.ACCEPTED)
        S5F2
          <B 0x0> .

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 5
    _function = 2

    _formatDescriptor = ACKC5()

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS06F00(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 00 - abort transaction stream 6

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F00()
        S6F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 6
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS06F05(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 05 - multi block data inquiry

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`

    **Structure**::

        {
            DATAID: A/I*/U*
            DATALENGTH: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F05({"DATAID": 1, "DATALENGTH": 1337})
        S6F5 W
          <L [2]
            <U4 1 >
            <I2 1337 >
          > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 5

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", DATAID()),
        ("DATALENGTH", SecsVarDynamic([SecsVarU1,
                                       SecsVarU2,
                                       SecsVarU4,
                                       SecsVarU8,
                                       SecsVarI1,
                                       SecsVarI2,
                                       SecsVarI4,
                                       SecsVarI8])),
    )), 2)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS06F06(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 06 - multi block data grant

    **Structure**::

        GRANT6: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F06(0)
        S6F6
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 6
    _function = 6

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS06F07(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 07 - data transfer request

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`

    **Structure**::

        {
            DATAID: A/I*/U*
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F07(1)
        S6F7 W
          <U4 1 > .

    :param value: parameters for this function (see example)
    :type value: integer
    """
    _stream = 6
    _function = 7

    _formatDescriptor = SecsVarU4(1)

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS06F08(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 08 - data transfer data

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`
    - :class:`CEID <secsgem.secs.dataitems.CEID>`

    **Structure**::

        {
            DATAID: A/I*/U*
            CEID: A/I*/U*
            DS: [
                {
                    DSID: U4[1]
                    DV: [
                        {
                            DVNAME: various
                            DVVAL: various
                        }
                         ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F08({"DATAID": 1, "CEID": 1337, "DS": [{"DSID": 1000, "DV": [{"DVNAME": "VAR1", "DVVAL": "VAR"}, {"DVNAME": "VAR2", "DVVAL": secsgem.SecsVarU4(value=100)}]}]})
        S6F8 W 
          <L [3]
            <U4 1 >
            <U4 1337 >
            <L [1]
              <L [2]
                <I2 1000 >
                <L [2]
                  <L [2]
                    <A "VAR1">
                    <A "VAR">
                  >
                  <L [2]
                    <A "VAR2">
                    <U4 100 >
                  >
                >
              >
            >
          > .

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 6
    _function = 8

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", DATAID()),
        ("CEID", CEID()),
        ("DS", SecsVarArray(
            SecsVarList(OrderedDict((
                ("DSID", SecsVarDynamic([SecsVarString,
                                         SecsVarU1,
                                         SecsVarU2,
                                         SecsVarU4,
                                         SecsVarU8,
                                         SecsVarI1,
                                         SecsVarI2,
                                         SecsVarI4,
                                         SecsVarI8])),
                ("DV", SecsVarArray(
                    SecsVarList(OrderedDict((
                        ("DVNAME", SecsVarDynamic([SecsVarString,
                                                   SecsVarU1,
                                                   SecsVarU2,
                                                   SecsVarU4,
                                                   SecsVarU8,
                                                   SecsVarI1,
                                                   SecsVarI2,
                                                   SecsVarI4,
                                                   SecsVarI8])),
                        ("DVVAL", SecsVarDynamic([SecsVarString,
                                                  SecsVarU1,
                                                  SecsVarU2,
                                                  SecsVarU4,
                                                  SecsVarU8,
                                                  SecsVarI1,
                                                  SecsVarI2,
                                                  SecsVarI4,
                                                  SecsVarI8])),
                    )), 2)
                )),
            )), 2)
        )),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS06F11(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 11 - event report

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`
    - :class:`CEID <secsgem.secs.dataitems.CEID>`
    - :class:`RPTID <secsgem.secs.dataitems.RPTID>`

    **Structure**::

        {
            DATAID: A/I*/U*
            CEID: A/I*/U*
            RPT: [
                {
                    RPTID: A/I*/U*
                    V: [
                        DATA: various
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F11({"DATAID": 1, "CEID": 1337, "RPT": [{"RPTID": 1000, "V": ["VAR", secsgem.SecsVarU4(value=100)]}]})
        S6F11 W
          <L [3]
            <U4 1 >
            <U4 1337 >
            <L [1]
              <L [2]
                <U4 1000 >
                <L [2]
                  <A "VAR">
                  <U4 100 >
                >
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 11

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", DATAID()),
        ("CEID", CEID()),
        ("RPT", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RPTID", RPTID()),
                ("V", SecsVarArray(
                    SecsVarDynamic([])
                )),
            )), 2)
        )),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS06F12(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 12 - event report - acknowledge

    **Structure**::

        ACKC6: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F12(0)
        S6F12
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 6
    _function = 12

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS06F15(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 15 - event report request

    **Data Items**

    - :class:`CEID <secsgem.secs.dataitems.CEID>`

    **Structure**::

        {
            CEID: A/I*/U*
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F15(1337)
        S6F15 W
            <U4 1337 >

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 15

    _formatDescriptor = CEID()

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS06F16(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 16 - event report data

    **Data Items**

    - :class:`DATAID <secsgem.secs.dataitems.DATAID>`
    - :class:`CEID <secsgem.secs.dataitems.CEID>`
    - :class:`RPTID <secsgem.secs.dataitems.RPTID>`

    **Structure**::

        {
            DATAID: A/I*/U*
            CEID: A/I*/U*
            RPT: [
                {
                    RPTID: A/I*/U*
                    V: [
                        DATA: various
                        ...
                    ]
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F16({"DATAID": 1, "CEID": 1337, "RPT": [{"RPTID": 1000, "V": ["VAR", secsgem.SecsVarU4(value=100)]}]})
        S6F16 W
          <L [3]
            <U4 1 >
            <U4 1337 >
            <L [1]
              <L [2]
                <U4 1000 >
                <L [2]
                  <A "VAR">
                  <U4 100 >
                >
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 16

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATAID", DATAID()),
        ("CEID", CEID()),
        ("RPT", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RPTID", RPTID()),
                ("V", SecsVarArray(
                    SecsVarDynamic([])
                )),
            )), 2)
        )),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS06F19(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 19 - individual report request

    **Data Items**

    - :class:`RPTID <secsgem.secs.dataitems.RPTID>`

    **Structure**::

        {
            RPTID: A/I*/U*
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F19(secsgem.SecsVarU4(value=1337))
        S6F19 W
          <U4 1337 > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 19

    _formatDescriptor = RPTID()

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS06F20(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 20 - individual report data

    **Structure**::

        {
            V: various
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F20(["ASD", 1337])
        S6F20
        <L [2]
            <A "ASD">
            <I2 1337 >
        > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 20

    _formatDescriptor = SecsVarArray(SecsVarDynamic([]))

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS06F21(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 21 - annotated individual report request

    **Data Items**

    - :class:`RPTID <secsgem.secs.dataitems.RPTID>`

    **Structure**::

        {
            RPTID: A/I*/U*
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F21(secsgem.SecsVarU4(value=1337))
        S6F21 W
          <U4 1337 > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 21

    _formatDescriptor = RPTID()

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS06F22(SecsStreamFunction):
    """Secs stream and function class for stream 06, function 22 - annotated individual report data

    **Data Items**

    - :class:`VID <secsgem.secs.dataitems.VID>`

    **Structure**::

        [
            {
                VID: A/I*/U*
                V: various
            }
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS06F22([{"VID": "VID1", "V": "ASD"}, {"VID": 2, "V": 1337}])
        S6F22
        <L [2]
            <L [2]
            <A "VID1">
            <A "ASD">
            >
            <L [2]
            <I1 2 >
            <I2 1337 >
            >
        > .

    :param value: parameters for this function (see example)
    :type value: list
    """
    _stream = 6
    _function = 22

    _formatDescriptor = SecsVarArray(
                            SecsVarList(OrderedDict((
                                ("VID", VID()),
                                ("V", SecsVarDynamic([])),
                            )), 2)
                        )
    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS07F00(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 00 - abort transaction stream 7

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F00()
        S7F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 7
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS07F01(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 01 - process program load - inquire

    **Structure**::

        {
            PPID: A[n]
            LENGTH: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F01({"PPID": "program", "LENGTH": 4})
        S7F1 W
          <L [2]
            <A "program">
            <U4 4 >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("PPID", SecsVarString()),
        ("LENGTH", SecsVarU4(1)),
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS07F02(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 02 - process program load - grant

    **Structure**::

        PPGNT: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F02(0)
        S7F2
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 2

    _formatDescriptor = SecsVarBinary(1)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS07F03(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 03 - process program - send

    **Structure**::

        {
            PPID: A[n]
            PPBODY: B[n]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F03({"PPID": "program", "PPBODY": "data"})
        S7F3 W
          <L [2]
            <A "program">
            <B 0x64 0x61 0x74 0x61>
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("PPID", SecsVarString()),
        ("PPBODY", SecsVarBinary()),
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS07F04(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 04 - process program - acknowledge

    **Structure**::

        ACKC7: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F04(0)
        S7F4
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 4

    _formatDescriptor = SecsVarBinary(1)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS07F05(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 05 - process program - request

    **Structure**::

        PPID: A[n]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F05("program")
        S7F5 W
          <A "program">

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 5

    _formatDescriptor = SecsVarString()

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS07F06(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 06 - process program - data

    **Structure**::

        {
            PPID: A[n]
            PPBODY: B[n]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F06({"PPID": "program", "PPBODY": "data"})
        S7F6
          <L [2]
            <A "program">
            <B 0x64 0x61 0x74 0x61>
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 6

    _formatDescriptor = SecsVarList(OrderedDict((
        ("PPID", SecsVarString()),
        ("PPBODY", SecsVarBinary()),
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS07F17(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 17 - delete process program - send

    **Structure**::

        [
            PPID: A[n]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F17(["program1", "program2"])
        S7F17 W
          <L [2]
            <A "program1">
            <A "program2">
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 17

    _formatDescriptor = SecsVarArray(SecsVarString())

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS07F18(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 18 - delete process program - acknowledge

    **Structure**::

        ACKC7: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F18(0)
        S7F18
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 7
    _function = 18

    _formatDescriptor = SecsVarBinary(1)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS07F19(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 19 - current equipment process program - request

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F19()
        S7F19 W

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 19

    _formatDescriptor = None

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS07F20(SecsStreamFunction):
    """Secs stream and function class for stream 07, function 20 - current equipment process program - data

    **Structure**::

        [
            PPID: A[n]
            ...
        ]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS07F20(["program1", "program2"])
        S7F20
          <L [2]
            <A "program1">
            <A "program2">
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 7
    _function = 20

    _formatDescriptor = SecsVarArray(SecsVarString())

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS09F00(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 00 - abort transaction stream 9

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F00()
        S9F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 9
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F01(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 01 - unrecognized device id

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F01("HEADERDATA")
        S9F1
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 1

    _formatDescriptor = SecsVarBinary(10)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F03(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 03 - unrecognized stream type

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F03("HEADERDATA")
        S9F3
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 3

    _formatDescriptor = SecsVarBinary(10)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F05(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 05 - unrecognized function type

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F05("HEADERDATA")
        S9F5
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 5

    _formatDescriptor = SecsVarBinary(10)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F07(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 07 - illegal data

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F07("HEADERDATA")
        S9F7
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 7

    _formatDescriptor = SecsVarBinary(10)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F09(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 09 - transaction timer timeout

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F09("HEADERDATA")
        S9F9
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 9

    _formatDescriptor = SecsVarBinary(10)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F11(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 11 - data too long

    **Structure**::

        MHEAD: B[10]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F11("HEADERDATA")
        S9F11
          <B 0x48 0x45 0x41 0x44 0x45 0x52 0x44 0x41 0x54 0x41>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 9
    _function = 11

    _formatDescriptor = SecsVarBinary(10)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS09F13(SecsStreamFunction):
    """Secs stream and function class for stream 09, function 13 - conversation timeout

    **Structure**::

        {
            MEXP: A[6]
            EDID: A[80]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS09F13({"MEXP": "S01E01", "EDID": "data"})
        S9F13
          <L [2]
            <A "S01E01">
            <A "data">
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 9
    _function = 13

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MEXP", SecsVarString(6)),
        ("EDID", SecsVarString(80)),
    )), 2)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS10F00(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 00 - abort transaction stream 10

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F00()
        S10F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 10
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS10F01(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 01 - terminal - request

    **Structure**::

        {
            TID: B[1]
            TEXT: A[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F01({"TID": 0, "TEXT": "hello?"})
        S10F1
          <L [2]
            <B 0x0>
            <A "hello?">
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 10
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("TID", SecsVarBinary(1)),
        ("TEXT", SecsVarString()),
    )), 2)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS10F02(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 02 - terminal - acknowledge

    **Structure**::

        ACK10: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F02(0)
        S10F2
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 10
    _function = 2

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS10F03(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 03 - terminal single - display

    **Structure**::

        {
            TID: B[1]
            TEXT: A[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F03({"TID": 0, "TEXT": "hello!"})
        S10F3
          <L [2]
            <B 0x0>
            <A "hello!">
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 10
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("TID", SecsVarBinary(1)),
        ("TEXT", SecsVarString()),
    )), 2)

    _toHost = False
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS10F04(SecsStreamFunction):
    """Secs stream and function class for stream 10, function 04 - terminal single - acknowledge

    **Structure**::

        ACK10: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS10F04(0)
        S10F4
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 10
    _function = 4

    _formatDescriptor = SecsVarBinary(1)

    _toHost = True
    _toEquipment = False

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F00(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 00 - abort transaction stream 12

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F00()
        S12F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 12
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F01(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 01 - map setup data - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            FNLOC: U2[1]
            FFROT: U2[1]
            ORLOC: B[1]
            RPSEL: U1[1]
            REF: [
                REFP: I4[2]
                ...
            ]
            DUTMS: A[n]
            XDIES: U4[1]
            YDIES: U4[1]
            ROWCT: U4[1]
            COLCT: U4[1]
            NULBC: A[n]
            PRDCT: U4[1]
            PRAXI: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F01({"MID": "materialID",
                "IDTYP": 0,
                "FNLOC": 0,
                "FFROT": 0,
                "ORLOC": 0,
                "RPSEL": 0,
                "REF": [[1,2], [2,3]],
                "DUTMS": "unit",
                "XDIES": 100,
                "YDIES": 100,
                "ROWCT": 10,
                "COLCT": 10,
                "NULBC": "{x}",
                "PRDCT": 100,
                "PRAXI": 0,
                })
        S12F1 W
          <L [15]
            <A "materialID">
            <B 0x0>
            <U2 0 >
            <U2 0 >
            <B 0x0>
            <U1 0 >
            <L [2]
              <I4 1 2 >
              <I4 2 3 >
            >
            <A "unit">
            <U4 100 >
            <U4 100 >
            <U4 10 >
            <U4 10 >
            <A "{x}">
            <U4 100 >
            <B 0x0>
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("FNLOC", SecsVarU2(1)),
        ("FFROT", SecsVarU2(1)),
        ("ORLOC", SecsVarBinary(1)),
        ("RPSEL", SecsVarU1(1)),
        ("REF", SecsVarArray(
            SecsVarI4(2)
        )),
        ("DUTMS", SecsVarString()),
        ("XDIES", SecsVarU4(1)),
        ("YDIES", SecsVarU4(1)),
        ("ROWCT", SecsVarU4(1)),
        ("COLCT", SecsVarU4(1)),
        ("NULBC", SecsVarDynamic([SecsVarString, SecsVarU1])),
        ("PRDCT", SecsVarU4(1)),
        ("PRAXI", SecsVarBinary(1)),
    )), 15)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS12F02(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 02 - map setup data - acknowledge

    **Structure**::

        SDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F02(0)
        S12F2
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 2

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F03(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 03 - map setup data - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            MAPFT: B[1]
            FNLOC: U2[1]
            FFROT: U2[1]
            ORLOC: B[1]
            PRAXI: B[1]
            BCEQU: U1[n]
            NULBC: A[n]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F03({"MID": "materialID",
                "IDTYP": 0,
                "MAPFT": 0,
                "FNLOC": 0,
                "FFROT": 0,
                "ORLOC": 0,
                "PRAXI": 0,
                "BCEQU": [1, 3, 5, 7],
                "NULBC": "{x}",
                })
        S12F3 W
          <L [9]
            <A "materialID">
            <B 0x0>
            <B 0x0>
            <U2 0 >
            <U2 0 >
            <B 0x0>
            <B 0x0>
            <U1 1 3 5 7 >
            <A "{x}">
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("MAPFT", SecsVarBinary(1)),
        ("FNLOC", SecsVarU2(1)),
        ("FFROT", SecsVarU2(1)),
        ("ORLOC", SecsVarBinary(1)),
        ("PRAXI", SecsVarBinary(1)),
        ("BCEQU", SecsVarU1()),
        ("NULBC", SecsVarDynamic([SecsVarString, SecsVarU1])),
    )), 9)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS12F04(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 04 - map setup data

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            FNLOC: U2[1]
            ORLOC: B[1]
            RPSEL: U1[1]
            REF: [
                REFP: I4[2]
                ...
            ]
            DUTMS: A[n]
            XDIES: U4[1]
            YDIES: U4[1]
            ROWCT: U4[1]
            COLCT: U4[1]
            PRDCT: U4[1]
            BCEQU: U1[n]
            NULBC: A[n]
            MLCL: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F04({"MID": "materialID",
                "IDTYP": 0,
                "FNLOC": 0,
                "ORLOC": 0,
                "RPSEL": 0,
                "REF": [[1,2], [2,3]],
                "DUTMS": "unit",
                "XDIES": 100,
                "YDIES": 100,
                "ROWCT": 10,
                "COLCT": 10,
                "PRDCT": 100,
                "BCEQU": [1, 3, 5, 7],
                "NULBC": "{x}",
                "MLCL": 0,
                })
        S12F4
          <L [15]
            <A "materialID">
            <B 0x0>
            <U2 0 >
            <B 0x0>
            <U1 0 >
            <L [2]
              <I4 1 2 >
              <I4 2 3 >
            >
            <A "unit">
            <U4 100 >
            <U4 100 >
            <U4 10 >
            <U4 10 >
            <U4 100 >
            <U1 1 3 5 7 >
            <A "{x}">
            <U4 0 >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 4

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("FNLOC", SecsVarU2(1)),
        ("ORLOC", SecsVarBinary(1)),
        ("RPSEL", SecsVarU1(1)),
        ("REF", SecsVarArray(
            SecsVarI4(2)
        )),
        ("DUTMS", SecsVarString()),
        ("XDIES", SecsVarU4(1)),
        ("YDIES", SecsVarU4(1)),
        ("ROWCT", SecsVarU4(1)),
        ("COLCT", SecsVarU4(1)),
        ("PRDCT", SecsVarU4(1)),
        ("BCEQU", SecsVarU1()),
        ("NULBC", SecsVarDynamic([SecsVarString, SecsVarU1])),
        ("MLCL", SecsVarU4(1)),
    )), 15)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F05(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 05 - map transmit inquire

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            MAPFT: B[1]
            MLCL: U4[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F05({"MID": "materialID", "IDTYP": 0, "MAPFT": 0, "MLCL": 0})
        S12F5 W
          <L [4]
            <A "materialID">
            <B 0x0>
            <B 0x0>
            <U4 0 >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 5

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("MAPFT", SecsVarBinary(1)),
        ("MLCL", SecsVarU4(1)),
    )), 4)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS12F06(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 06 - map transmit - grant

    **Structure**::

        GRNT1: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F06(0)
        S12F6
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 6

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F07(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 07 - map data type 1 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    RSINF: I4[3]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F07({"MID": "materialID", "IDTYP": 0, "DATA": [{"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F7 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I4 1 2 3 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I4 4 5 6 >
                <U1 5 6 7 8 >
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 7

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RSINF", SecsVarI4(3)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS12F08(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 08 - map data type 1 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F08(0)
        S12F8
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 8

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F09(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 09 - map data type 2 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            STRP: I2[2]
            BINLT: U1[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F09({"MID": "materialID", "IDTYP": 0, "STRP": [0, 1], "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F9 W
          <L [4]
            <A "materialID">
            <B 0x0>
            <I2 0 1 >
            <U1 1 2 3 4 5 6 >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 9

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("STRP", SecsVarI2(2)),
        ("BINLT", SecsVarU1()),
    )), 4)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS12F10(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 10 - map data type 2 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F10(0)
        S12F10
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 10

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F11(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 11 - map data type 3 - send

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    XYPOS: I2[2]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F11({"MID": "materialID", "IDTYP": 0, "DATA": [{"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F11 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I2 1 2 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I2 3 4 >
                <U1 5 6 7 8 >
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 11

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("XYPOS", SecsVarI2(2)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = True


class SecsS12F12(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 12 - map data type 3 - acknowledge

    **Structure**::

        MDACK: B[1]

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F12(0)
        S12F12
          <B 0x0>

    :param value: parameters for this function (see example)
    :type value: byte
    """
    _stream = 12
    _function = 12

    _formatDescriptor = SecsVarBinary(1)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS12F13(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 13 - map data type 1 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F13({"MID": "materialID", "IDTYP": 0})
        S12F13 W
          <L [2]
            <A "materialID">
            <B 0x0>
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 13

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
    )), 2)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS12F14(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 14 - map data type 1

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    RSINF: I4[3]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F14({"MID": "materialID", "IDTYP": 0, "DATA": [{"RSINF": [1, 2, 3], "BINLT": [1, 2, 3, 4]}, {"RSINF": [4, 5, 6], "BINLT": [5, 6, 7, 8]}]})
        S12F14
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I4 1 2 3 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I4 4 5 6 >
                <U1 5 6 7 8 >
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 14

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("RSINF", SecsVarI4(3)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS12F15(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 15 - map data type 2 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F15({"MID": "materialID", "IDTYP": 0})
        S12F15 W
          <L [2]
            <A "materialID">
            <B 0x0>
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 15

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
    )), 2)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS12F16(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 16 - map data type 2

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            STRP: I2[2]
            BINLT: U1[]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F16({"MID": "materialID", "IDTYP": 0, "STRP": [0, 1], "BINLT": [1, 2, 3, 4, 5, 6]})
        S12F16
          <L [4]
            <A "materialID">
            <B 0x0>
            <I2 0 1 >
            <U1 1 2 3 4 5 6 >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 16

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("STRP", SecsVarI2(2)),
        ("BINLT", SecsVarU1()),
    )), 4)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS12F17(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 17 - map data type 3 - request

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            SDBIN: B[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F17({"MID": "materialID", "IDTYP": 0, "SDBIN": 1})
        S12F17 W
          <L [3]
            <A "materialID">
            <B 0x0>
            <B 0x1>
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 17

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("SDBIN", SecsVarBinary(1)),
    )), 3)

    _toHost = True
    _toEquipment = False

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS12F18(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 18 - map data type 3

    **Structure**::

        {
            MID: A[16]
            IDTYP: B[1]
            [
                {
                    XYPOS: I2[2]
                    BINLT: U1[]
                }
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F18({"MID": "materialID", "IDTYP": 0, "DATA": [{"XYPOS": [1, 2], "BINLT": [1, 2, 3, 4]}, {"XYPOS": [3, 4], "BINLT": [5, 6, 7, 8]}]})
        S12F18
          <L [3]
            <A "materialID">
            <B 0x0>
            <L [2]
              <L [2]
                <I2 1 2 >
                <U1 1 2 3 4 >
              >
              <L [2]
                <I2 3 4 >
                <U1 5 6 7 8 >
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 18

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MID", SecsVarString(16)),
        ("IDTYP", SecsVarBinary(1)),
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("XYPOS", SecsVarI2(2)),
                ("BINLT", SecsVarU1()),
            )), 2)
        )),
    )), 3)

    _toHost = False
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS12F19(SecsStreamFunction):
    """Secs stream and function class for stream 12, function 19 - map error report - send

    **Structure**::

        {
            MAPER: B[1]
            DATLC: U1[1]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS12F19({"MAPER": 1, "DATLC": 0})
        S12F19
          <L [2]
            <B 0x1>
            <U1 0 >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 12
    _function = 19

    _formatDescriptor = SecsVarList(OrderedDict((
        ("MAPER", SecsVarBinary(1)),
        ("DATLC", SecsVarU1(1)),
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS14F00(SecsStreamFunction):
    """Secs stream and function class for stream 14, function 00 - abort transaction stream 14

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS14F00()
        S14F0

    :param value: function has no parameters
    :type value: None
    """
    _stream = 14
    _function = 0

    _formatDescriptor = None

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = False


class SecsS14F01(SecsStreamFunction):
    """Secs stream and function class for stream 14, function 01 - GetAttr request

    **Structure**::

        {
            OBJSPEC: A[]
            OBJTYPE: various
            OBJID: [
                DATA: various
                ...
            ]
            FILTER: [
                {
                    ATTRID: various
                    ATTRDATA: various
                    ATTRRELN: U1[]
                }
                ...
            ]
            ATTRID: [
                DATA: various
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS14F01({"OBJSPEC": '', "OBJTYPE": 'StripMap', "OBJID": ['MAP001'], "FILTER": [], "ATTRID": ['OriginLocation', 'Rows', 'Columns', 'CellStatus', 'LotID']})
        S14F1 W
          <L [5]
            <A>
            <A "StripMap">
            <L [1]
              <A "MAP001">
            >
            <L>
            <L [5]
              <A "OriginLocation">
              <A "Rows">
              <A "Columns">
              <A "CellStatus">
              <A "LotID">
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 14
    _function = 1

    _formatDescriptor = SecsVarList(OrderedDict((
        ("OBJSPEC", SecsVarString()),
        ("OBJTYPE", SecsVarDynamic([SecsVarString,
                                    SecsVarU1,
                                    SecsVarU2,
                                    SecsVarU4,
                                    SecsVarU8])),
        ("OBJID", SecsVarArray(SecsVarDynamic([SecsVarString,
                                               SecsVarU1,
                                               SecsVarU2,
                                               SecsVarU4,
                                               SecsVarU8]))),
        ("FILTER", SecsVarArray(
            SecsVarList(OrderedDict((
                ("ATTRID", SecsVarDynamic([SecsVarString,
                                           SecsVarU1,
                                           SecsVarU2,
                                           SecsVarU4,
                                           SecsVarU8])),
                ("ATTRDATA", SecsVarDynamic([])),
                ("ATTRRELN", SecsVarU1(1)),
            )), 3)
        )),
        ("ATTRID", SecsVarArray(SecsVarDynamic([SecsVarString,
                                                SecsVarU1,
                                                SecsVarU2,
                                                SecsVarU4,
                                                SecsVarU8]))),
    )), 5)

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False

    RELATION = {
        "EQUAL": 0,
        "NOTEQUAL": 1,
        "LESS": 2,
        "LESSEQUAL": 3,
        "GREATER": 4,
        "GREATEREQUAL": 5,
        "PRESENT": 6,
        "NOTPRESENT": 7,
    }


class SecsS14F02(SecsStreamFunction):
    """Secs stream and function class for stream 14, function 02 - GetAttr data

    **Structure**::

        {
            DATA: [
                {
                    OBJID: various
                    ATTRIBS: [
                        {
                            ATTRID: various
                            ATTRDATA: various
                        }
                        ...
                    ]
                }
                ...
            ]
            ERRORS: {
                OBJACK: U1
                ERROR: [
                    {
                        ERRCODE: various
                        ERRTEXT: A[]
                    }
                    ...
                ]
            }
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS14F02({"DATA": [{"OBJID": "MAP001", "ATTRIBS": [{"ATTRID": "OriginLocation", "ATTRDATA": "0"},{"ATTRID": "Rows", "ATTRDATA": 4},{"ATTRID": "Columns", "ATTRDATA": 4},{"ATTRID": "CellStatus", "ATTRDATA": 6},{"ATTRID": "LotID", "ATTRDATA":"LOT001"}]}], "ERRORS": {"OBJACK": 0}})
        S14F2
          <L [2]
            <L [1]
              <L [2]
                <A "MAP001">
                <L [5]
                  <L [2]
                    <A "OriginLocation">
                    <A "0">
                  >
                  <L [2]
                    <A "Rows">
                    <A "4">
                  >
                  <L [2]
                    <A "Columns">
                    <A "4">
                  >
                  <L [2]
                    <A "CellStatus">
                    <A "6">
                  >
                  <L [2]
                    <A "LotID">
                    <A "LOT001">
                  >
                >
              >
            >
            <L [2]
              <U1 0 >
              <L>
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 14
    _function = 2

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("OBJID", SecsVarDynamic([SecsVarString,
                                          SecsVarU1,
                                          SecsVarU2,
                                          SecsVarU4,
                                          SecsVarU8])),
                ("ATTRIBS", SecsVarArray(
                    SecsVarList(OrderedDict((
                        ("ATTRID", SecsVarDynamic([SecsVarString,
                                                   SecsVarU1,
                                                   SecsVarU2,
                                                   SecsVarU4,
                                                   SecsVarU8])),
                        ("ATTRDATA", SecsVarDynamic([])),
                    )), 2)
                )),
            )), 2)
        )),
        ("ERRORS", SecsVarList(OrderedDict((
            ("OBJACK", SecsVarU1(1)),
            ("ERROR", SecsVarArray(
                SecsVarList(OrderedDict((
                    ("ERRCODE", SecsVarDynamic([SecsVarU1,
                                                SecsVarU2,
                                                SecsVarU4,
                                                SecsVarU8])),
                    ("ERRTEXT", SecsVarString()),
                )), 2)
            )),
        )), 2)),
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


class SecsS14F03(SecsStreamFunction):
    """Secs stream and function class for stream 14, function 03 - SetAttr request

    **Structure**::

        {
            OBJSPEC: A[]
            OBJTYPE: various
            OBJID: [
                DATA: various
                ...
            ]
            ATTRIBS: [
                {
                    ATTRID: various
                    ATTRDATA: various
                }
                ...
            ]
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS14F03({"OBJSPEC": '', "OBJTYPE": 'StripMap', "OBJID": ['MAP001'], "ATTRIBS": [ {"ATTRID": "CellStatus", "ATTRDATA": 3} ] })
        S14F3 W
          <L [4]
            <A>
            <A "StripMap">
            <L [1]
              <A "MAP001">
            >
            <L [1]
              <L [2]
                <A "CellStatus">
                <A "3">
              >
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 14
    _function = 3

    _formatDescriptor = SecsVarList(OrderedDict((
        ("OBJSPEC", SecsVarString()),
        ("OBJTYPE", SecsVarDynamic([SecsVarString,
                                    SecsVarU1,
                                    SecsVarU2,
                                    SecsVarU4,
                                    SecsVarU8])),
        ("OBJID", SecsVarArray(SecsVarDynamic([SecsVarString,
                                               SecsVarU1,
                                               SecsVarU2,
                                               SecsVarU4,
                                               SecsVarU8]))),
        ("ATTRIBS", SecsVarArray(
            SecsVarList(OrderedDict((
                ("ATTRID", SecsVarDynamic([SecsVarString,
                                           SecsVarU1,
                                           SecsVarU2,
                                           SecsVarU4,
                                           SecsVarU8])),
                ("ATTRDATA", SecsVarDynamic([])),
            )), 2)
        )),
    )), 4)

    _toHost = True
    _toEquipment = True

    _hasReply = True
    _isReplyRequired = True

    _isMultiBlock = False


class SecsS14F04(SecsStreamFunction):
    """Secs stream and function class for stream 14, function 04 - SetAttr data

    **Structure**::

        {
            DATA: [
                {
                    OBJID: various
                    ATTRIBS: [
                        {
                            ATTRID: various
                            ATTRDATA: various
                        }
                        ...
                    ]
                }
                ...
            ]
            ERRORS: {
                OBJACK: U1
                ERROR: [
                    {
                        ERRCODE: various
                        ERRTEXT: A[]
                    }
                    ...
                ]
            }
        }

    **Example**::

        >>> import secsgem
        >>> secsgem.SecsS14F04({"DATA": [{"OBJID": "MAP001", "ATTRIBS": [{"ATTRID": "OriginLocation", "ATTRDATA": "0"},{"ATTRID": "Rows", "ATTRDATA": 4},{"ATTRID": "Columns", "ATTRDATA": 4},{"ATTRID": "CellStatus", "ATTRDATA": 6},{"ATTRID": "LotID", "ATTRDATA":"LOT001"}]}], "ERRORS": {"OBJACK": 0}})
        S14F4
          <L [2]
            <L [1]
              <L [2]
                <A "MAP001">
                <L [5]
                  <L [2]
                    <A "OriginLocation">
                    <A "0">
                  >
                  <L [2]
                    <A "Rows">
                    <A "4">
                  >
                  <L [2]
                    <A "Columns">
                    <A "4">
                  >
                  <L [2]
                    <A "CellStatus">
                    <A "6">
                  >
                  <L [2]
                    <A "LotID">
                    <A "LOT001">
                  >
                >
              >
            >
            <L [2]
              <U1 0 >
              <L>
            >
          >

    :param value: parameters for this function (see example)
    :type value: dict
    """
    _stream = 14
    _function = 4

    _formatDescriptor = SecsVarList(OrderedDict((
        ("DATA", SecsVarArray(
            SecsVarList(OrderedDict((
                ("OBJID", SecsVarDynamic([SecsVarString,
                                          SecsVarU1,
                                          SecsVarU2,
                                          SecsVarU4,
                                          SecsVarU8])),
                ("ATTRIBS", SecsVarArray(
                    SecsVarList(OrderedDict((
                        ("ATTRID", SecsVarDynamic([SecsVarString,
                                                   SecsVarU1,
                                                   SecsVarU2,
                                                   SecsVarU4,
                                                   SecsVarU8])),
                        ("ATTRDATA", SecsVarDynamic([])),
                    )), 2)
                )),
            )), 2)
        )),
        ("ERRORS", SecsVarList(OrderedDict((
            ("OBJACK", SecsVarU1(1)),
            ("ERROR", SecsVarArray(
                SecsVarList(OrderedDict((
                    ("ERRCODE", SecsVarDynamic([SecsVarU1,
                                                SecsVarU2,
                                                SecsVarU4,
                                                SecsVarU8])),
                    ("ERRTEXT", SecsVarString()),
                )), 2)
            )),
        )), 2)),
    )), 2)

    _toHost = True
    _toEquipment = True

    _hasReply = False
    _isReplyRequired = False

    _isMultiBlock = True


secsStreamsFunctions = {
    0: {
        0: SecsS00F00,
    },
    1: {
        0: SecsS01F00,
        1: SecsS01F01,
        2: SecsS01F02,
        3: SecsS01F03,
        4: SecsS01F04,
        11: SecsS01F11,
        12: SecsS01F12,
        13: SecsS01F13,
        14: SecsS01F14,
        15: SecsS01F15,
        16: SecsS01F16,
        17: SecsS01F17,
        18: SecsS01F18,
    },
    2: {
        0: SecsS02F00,
        13: SecsS02F13,
        14: SecsS02F14,
        15: SecsS02F15,
        16: SecsS02F16,
        17: SecsS02F17,
        18: SecsS02F18,
        29: SecsS02F29,
        30: SecsS02F30,
        33: SecsS02F33,
        34: SecsS02F34,
        35: SecsS02F35,
        36: SecsS02F36,
        37: SecsS02F37,
        38: SecsS02F38,
        41: SecsS02F41,
        42: SecsS02F42,
    },
    5: {
        0: SecsS05F00,
        1: SecsS05F01,
        2: SecsS05F02,
    },
    6: {
        0: SecsS06F00,
        5: SecsS06F05,
        6: SecsS06F06,
        7: SecsS06F07,
        8: SecsS06F08,
        11: SecsS06F11,
        12: SecsS06F12,
        15: SecsS06F15,
        16: SecsS06F16,
        19: SecsS06F19,
        20: SecsS06F20,
        21: SecsS06F21,
        22: SecsS06F22,
    },
    7: {
        1: SecsS07F01,
        2: SecsS07F02,
        3: SecsS07F03,
        4: SecsS07F04,
        5: SecsS07F05,
        6: SecsS07F06,
        17: SecsS07F17,
        18: SecsS07F18,
        19: SecsS07F19,
        20: SecsS07F20,
    },
    9: {
        0: SecsS09F00,
        1: SecsS09F01,
        3: SecsS09F03,
        5: SecsS09F05,
        7: SecsS09F07,
        9: SecsS09F09,
        11: SecsS09F11,
        13: SecsS09F13,
    },
    10: {
        0: SecsS10F00,
        1: SecsS10F01,
        2: SecsS10F02,
        3: SecsS10F03,
        4: SecsS10F04,
    },
    12: {
        0: SecsS12F00,
        1: SecsS12F01,
        2: SecsS12F02,
        3: SecsS12F03,
        4: SecsS12F04,
        5: SecsS12F05,
        6: SecsS12F06,
        7: SecsS12F07,
        8: SecsS12F08,
        9: SecsS12F09,
        10: SecsS12F10,
        11: SecsS12F11,
        12: SecsS12F12,
        13: SecsS12F13,
        14: SecsS12F14,
        15: SecsS12F15,
        16: SecsS12F16,
        17: SecsS12F17,
        18: SecsS12F18,
        19: SecsS12F19,
    },
    14: {
        0: SecsS14F00,
        1: SecsS14F01,
        2: SecsS14F02,
        3: SecsS14F03,
        4: SecsS14F04,
    },
}
