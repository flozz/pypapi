"""
Some constants used by PAPI.

.. NOTE::

    Event contants are located in an other file, see :doc:events
"""

from ctypes import c_int

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


# PAPI Mask

#: Mask to indicate the event is a native event
PAPI_NATIVE_MASK = c_int(lib.PAPI_NATIVE_MASK).value

#: Mask to indicate the event is a preset event
PAPI_PRESET_MASK = c_int(lib.PAPI_PRESET_MASK).value


# PAPI Option

#: For small strings, like names & stuff
PAPI_MIN_STR_LEN = lib.PAPI_MIN_STR_LEN

#: For average run-of-the-mill strings
PAPI_MAX_STR_LEN = lib.PAPI_MAX_STR_LEN

#: For somewhat longer run-of-the-mill strings
PAPI_2MAX_STR_LEN = lib.PAPI_2MAX_STR_LEN

#: This should be defined in terms of a system parameter
PAPI_HUGE_STR_LEN = lib.PAPI_HUGE_STR_LEN

#: Dhould match PAPI_EVENTS_IN_DERIVED_EVENT defined in papi_internal.h
PAPI_MAX_INFO_TERMS = lib.PAPI_MAX_INFO_TERMS


# PAPI Error

#: Option to turn off automatic reporting of return codes < 0 to stderr.
PAPI_QUIET = lib.PAPI_QUIET

#: Option to automatically report any return codes < 0 to stderr and continue
PAPI_VERB_ECONT = lib.PAPI_VERB_ECONT

#: Option to automatically report any return codes < 0 to stderr and exit.
PAPI_VERB_ESTOP = lib.PAPI_VERB_ESTOP


# PAPI Domain

#: User context counted
PAPI_DOM_USER = lib.PAPI_DOM_USER

#: Same as PAPI_DOM_USER
PAPI_DOM_MIN = PAPI_DOM_USER

#: Kernel/OS context counted
PAPI_DOM_KERNEL = lib.PAPI_DOM_KERNEL

#: Exception/transient mode (like user TLB misses)
PAPI_DOM_OTHER = lib.PAPI_DOM_OTHER

#: Supervisor/hypervisor context counted
PAPI_DOM_SUPERVISOR = lib.PAPI_DOM_SUPERVISOR

#: All contexts counted
PAPI_DOM_ALL = (
    lib.PAPI_DOM_USER
    | lib.PAPI_DOM_KERNEL
    | lib.PAPI_DOM_OTHER
    | lib.PAPI_DOM_SUPERVISOR
)

#: Same as PAPI_DOM_ALL
PAPI_DOM_MAX = PAPI_DOM_ALL

#: Flag that indicates we are not reading CPU like stuff. The lower 31 bits can be decoded by the component into something meaningful. i.e. SGI HUB counters
PAPI_DOM_HWSPEC = lib.PAPI_DOM_HWSPEC


# PAPI Granularity

#: PAPI counters for each individual thread
PAPI_GRN_THR = lib.PAPI_GRN_THR

#: Same as PAPI_GRN_THR
PAPI_GRN_MIN = PAPI_GRN_THR

#: PAPI counters for each individual process
PAPI_GRN_PROC = lib.PAPI_GRN_PROC

#: PAPI counters for each individual process group
PAPI_GRN_PROCG = lib.PAPI_GRN_PROCG

#: PAPI counters for the current CPU, are you bound?
PAPI_GRN_SYS = lib.PAPI_GRN_SYS

#: PAPI counters for all CPUs individually
PAPI_GRN_SYS_CPU = lib.PAPI_GRN_SYS_CPU

#: Same as PAPI_GRN_SYS_CPU
PAPI_GRN_MAX = PAPI_GRN_SYS_CPU


# PAPI Locking Mechanisms

#: User controlled locks
PAPI_USR1_LOCK = lib.PAPI_USR1_LOCK

#: User controlled locks
PAPI_USR2_LOCK = lib.PAPI_USR2_LOCK

#: Used with setting up array
PAPI_NUM_LOCK = lib.PAPI_NUM_LOCK

#: Same as PAPI_USR1_LOCK
PAPI_LOCK_USR1 = PAPI_USR1_LOCK

#: Same as PAPI_USR2_LOCK
PAPI_LOCK_USR2 = PAPI_USR2_LOCK

#: Same as PAPI_NUM_LOCK
PAPI_LOCK_NUM = PAPI_NUM_LOCK

# PAPI FLIPS/FLOPS

#: Floating point instructions executed
PAPI_FP_INS = lib.PAPI_FP_INS | PAPI_PRESET_MASK

#: Single precision vector/SIMD instructions
PAPI_VEC_SP = lib.PAPI_VEC_SP | PAPI_PRESET_MASK

#: Double precision vector/SIMD instructions
PAPI_VEC_DP = lib.PAPI_VEC_DP | PAPI_PRESET_MASK

#: Floating point operations executed
PAPI_FP_OPS = lib.PAPI_FP_OPS | PAPI_PRESET_MASK

#: Floating point operations executed; optimized to count scaled single precision vector operations
PAPI_SP_OPS = lib.PAPI_SP_OPS | PAPI_PRESET_MASK

#: Floating point operations executed; optimized to count scaled double precision vector operations
PAPI_DP_OPS = lib.PAPI_DP_OPS | PAPI_PRESET_MASK


# Others

#: A nonexistent hardware event used as a placeholder
PAPI_NULL = lib.PAPI_NULL
