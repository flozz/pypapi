"""
Some constants used by PAPI.

.. NOTE::

    Event contants are located in an other file, see :doc:events
"""


from ._papi import lib


# Version

def _papi_version_number(maj, min_, rev, inc):
    return maj << 24 | min_ << 16 | rev << 8 | inc


#: PAPI version, as used internaly
PAPI_VERSION = _papi_version_number(5, 5, 1, 0)

#: PAPI version, without the revision and increment part
PAPI_VER_CURRENT = PAPI_VERSION & 0xFFFF0000


# PAPI Instialization

#: PAPI is not initilized
PAPI_NOT_INITED = lib.PAPI_NOT_INITED

#: Low level has called library init
PAPI_LOW_LEVEL_INITED = lib.PAPI_LOW_LEVEL_INITED

#: High level has called library init
PAPI_HIGH_LEVEL_INITED = lib.PAPI_HIGH_LEVEL_INITED

#: Threads have been inited
PAPI_THREAD_LEVEL_INITED = lib.PAPI_THREAD_LEVEL_INITED
