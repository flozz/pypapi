"""
Some constants used by PAPI.

.. NOTE::

    Event contants are located in an other file, see :doc:events
"""


import numpy as np

from ._papi import lib


# Version


def _papi_version_number(maj, min_, rev, inc):
    return maj << 24 | min_ << 16 | rev << 8 | inc


#: PAPI version, as used internaly
PAPI_VERSION = _papi_version_number(6, 0, 0, 1)

#: PAPI version, without the revision and increment part
PAPI_VER_CURRENT = PAPI_VERSION & 0xFFFF0000


# PAPI Initialization

#: PAPI is not initilized
PAPI_NOT_INITED = lib.PAPI_NOT_INITED

#: Low level has called library init
PAPI_LOW_LEVEL_INITED = lib.PAPI_LOW_LEVEL_INITED

#: High level has called library init
PAPI_HIGH_LEVEL_INITED = lib.PAPI_HIGH_LEVEL_INITED

#: Threads have been inited
PAPI_THREAD_LEVEL_INITED = lib.PAPI_THREAD_LEVEL_INITED


# PAPI State

#: EventSet stopped
PAPI_STOPPED = lib.PAPI_STOPPED

#: EventSet running
PAPI_RUNNING = lib.PAPI_RUNNING

#: EventSet temp. disabled by the library
PAPI_PAUSED = lib.PAPI_PAUSED

#: EventSet defined, but not initialized
PAPI_NOT_INIT = lib.PAPI_NOT_INIT

#: EventSet has overflowing enabled
PAPI_OVERFLOWING = lib.PAPI_OVERFLOWING

#: EventSet has profiling enabled
PAPI_PROFILING = lib.PAPI_PROFILING

#: EventSet has multiplexing enabled
PAPI_MULTIPLEXING = lib.PAPI_MULTIPLEXING

#: EventSet is attached to another thread/process
PAPI_ATTACHED = lib.PAPI_ATTACHED

#: EventSet is attached to a specific cpu (not counting thread of execution)
PAPI_CPU_ATTACHED = lib.PAPI_CPU_ATTACHED


# Others

#: A nonexistent hardware event used as a placeholder
PAPI_NULL = lib.PAPI_NULL

# Masks
PAPI_NATIVE_MASK = np.intc(lib.PAPI_NATIVE_MASK)
PAPI_PRESET_MASK = np.uintc(lib.PAPI_PRESET_MASK).astype(np.intc)

# Option definitions
PAPI_MIN_STR_LEN = lib.PAPI_MIN_STR_LEN
PAPI_MAX_STR_LEN = lib.PAPI_MAX_STR_LEN
PAPI_2MAX_STR_LEN = lib.PAPI_2MAX_STR_LEN
PAPI_HUGE_STR_LEN = lib.PAPI_HUGE_STR_LEN

PAPI_MAX_INFO_TERMS = lib.PAPI_MAX_INFO_TERMS	

# Debug Level
PAPI_QUIET = lib.PAPI_QUIET
PAPI_VERB_ECONT = lib.PAPI_VERB_ECONT
PAPI_VERB_ESTOP = lib.PAPI_VERB_ESTOP

# Domain definitions
PAPI_DOM_USER = lib.PAPI_DOM_USER
PAPI_DOM_MIN = PAPI_DOM_USER
PAPI_DOM_KERNEL = lib.PAPI_DOM_KERNEL
PAPI_DOM_OTHER = lib.PAPI_DOM_OTHER
PAPI_DOM_SUPERVISOR = lib.PAPI_DOM_SUPERVISOR
PAPI_DOM_ALL = (lib.PAPI_DOM_USER|lib.PAPI_DOM_KERNEL|lib.PAPI_DOM_OTHER|lib.PAPI_DOM_SUPERVISOR)
PAPI_DOM_MAX = PAPI_DOM_ALL
PAPI_DOM_HWSPEC = lib.PAPI_DOM_HWSPEC

# Granularity definitions
PAPI_GRN_THR = lib.PAPI_GRN_THR
PAPI_GRN_MIN = PAPI_GRN_THR
PAPI_GRN_PROC = lib.PAPI_GRN_PROC
PAPI_GRN_PROCG = lib.PAPI_GRN_PROCG
PAPI_GRN_SYS = lib.PAPI_GRN_SYS
PAPI_GRN_SYS_CPU = lib.PAPI_GRN_SYS_CPU
PAPI_GRN_MAX = PAPI_GRN_SYS_CPU

# Locking Mechanisms
PAPI_USR1_LOCK = lib.PAPI_USR1_LOCK
PAPI_USR2_LOCK = lib.PAPI_USR2_LOCK
PAPI_NUM_LOCK = lib.PAPI_NUM_LOCK
PAPI_LOCK_USR1 = PAPI_USR1_LOCK
PAPI_LOCK_USR2 = PAPI_USR2_LOCK
PAPI_LOCK_NUM = PAPI_NUM_LOCK

# Flops values
PAPI_FP_INS = lib.PAPI_FP_INS|PAPI_PRESET_MASK
PAPI_VEC_SP = lib.PAPI_VEC_SP|PAPI_PRESET_MASK
PAPI_VEC_DP = lib.PAPI_VEC_DP|PAPI_PRESET_MASK
PAPI_FP_OPS = lib.PAPI_FP_OPS|PAPI_PRESET_MASK
PAPI_SP_OPS = lib.PAPI_SP_OPS|PAPI_PRESET_MASK
PAPI_DP_OPS = lib.PAPI_DP_OPS|PAPI_PRESET_MASK
