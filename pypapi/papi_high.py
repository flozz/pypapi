"""
This module binds `PAPI High Level API
<https://github.com/icl-utk-edu/papi/wiki/PAPI-HL>`_.

Example using the High Level API:

::

    from pypapi import papi_high

    papi_high.hl_region_begin("computation")

    # computation

    papi_high.hl_region_end("computation")


To change where results are stored or which events to record is achieved with
environment variables.

Bash:

.. code-block:: bash

    export PAPI_EVENTS="PAPI_TOT_INS,PAPI_TOT_CYC"
    export PAPI_OUTPUT_DIRECTORY="path/to/output"


Python::

    import os

    os.environ["PAPI_EVENTS"] = "PAPI_TOT_INS,PAPI_TOT_CYC"
    os.environ["PAPI_OUTPUT_DIRECTORY"] = "path/to/output"

"""

from ._papi import lib, ffi
from .exceptions import papi_error


# int PAPI_hl_region_begin(const char* region); /**< read performance events at the beginning of a region */
@papi_error
def hl_region_begin(region):
    """Read performance events at the beginning of a region.

    :param string region: name of instrumented region

    :returns: Operation status
    :rtype: int

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI.
    """
    cregion = ffi.new("char[]", region.encode("ascii"))
    rcode = lib.PAPI_hl_region_begin(cregion)
    return rcode, rcode


# int PAPI_hl_read(const char* region);
@papi_error
def hl_read(region):
    """Read performance events inside of a region and store the difference to
    the corresponding beginning of the region.

    :param string region: name of instrumented region

    :returns: Operation status
    :rtype: int

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI.
    """
    cregion = ffi.new("char[]", region.encode("ascii"))
    rcode = lib.PAPI_hl_read(cregion)
    return rcode, rcode


# int PAPI_hl_region_end(const char* region);
@papi_error
def hl_region_end(region):
    """Read performance events at the end of a region and store the difference
    to the corresponding beginning of the region.

    :param string region: name of instrumented region

    :returns: Operation status
    :rtype: int

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI.
    """
    cregion = ffi.new("char[]", region.encode("ascii"))
    rcode = lib.PAPI_hl_region_end(cregion)
    return rcode, rcode


# int PAPI_hl_stop();
@papi_error
def hl_stop():
    """Stops a running high-level event set.

    :returns: Operation status
    :rtype: int

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI.
    """
    rcode = lib.PAPI_hl_stop()
    return rcode, rcode
