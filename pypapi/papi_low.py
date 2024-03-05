"""
This module binds the PAPI Low Level API.

Despite our desire to stay as close as possible as the original C API, we had
to make a lot of change to make this API more *pythonic*. If you are used to
the C API, please read carefully this documentation.

Simple example::

    from pypapi import papi_low as papi
    from pypapi import events

    papi.library_init()

    evs = papi.create_eventset()
    papi.add_event(evs, events.PAPI_FP_OPS)

    papi.start(evs)

    # Do some computation here

    result = papi.stop(evs)
    print(result)

    papi.cleanup_eventset(evs)
    papi.destroy_eventset(evs)

.. NOTE::

    This binding is currently very partial, there is a lot of missing function.
    If you need one of the missing functions, please `fill an issue on Github
    <https://github.com/flozz/pypapi/issues>`_.
"""

from ctypes import c_longlong, c_ulonglong

from ._papi import lib, ffi
from .exceptions import papi_error, PapiError, PapiInvalidValueError
from .consts import (
    PAPI_VER_CURRENT,
    PAPI_NULL,
    PAPI_PRESET_MASK,
    PAPI_NATIVE_MASK,
    PAPI_MAX_STR_LEN,
)
from .structs import (
    EVENT_info,
    HARDWARE_info,
    DMEM_info,
    EXECUTABLE_info,
    COMPONENT_info,
    SHARED_LIB_info,
    Flips,
    Flops,
    IPC,
    EPC,
)


# int PAPI_accum(int EventSet, long long * values);
@papi_error
def accum(eventSet, values):
    """Adds the counters of the indicated event set into the array values. The
    counters are zeroed and continue counting after the operation.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param list(int) values: A list to hold the counter values of the counting
        events.

    :rtype: list(int)

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see
        the errno variable.
    :raises PapiNoEventSetError: The event set specified does not exist.
    """
    eventCount_p = ffi.new("int*", 0)
    rcode = lib.PAPI_list_events(eventSet, ffi.NULL, eventCount_p)

    if rcode < 0:
        return rcode, None

    eventCount = ffi.unpack(eventCount_p, 1)[0]

    if len(values) != eventCount:
        raise PapiInvalidValueError(
            message="the length of the 'value' list "
            "(%i) is different of the one of "
            "the event set (%i)" % (len(values), eventCount)
        )

    values = ffi.new("long long[]", values)

    rcode = lib.PAPI_accum(eventSet, values)

    return rcode, ffi.unpack(values, eventCount)


# int PAPI_add_event(int EventSet, int Event);
@papi_error
def add_event(eventSet, eventCode):
    """Add single PAPI preset or native hardware event to an event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int eventCode: A defined event such as ``PAPI_TOT_INS`` (from
        :doc:`events`).

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    :raises PapiBugError: Internal error, please send mail to the developers.
    """
    rcode = lib.PAPI_add_event(eventSet, eventCode)

    if rcode > 0:
        raise PapiError(
            message="Unable to add some of the given events: %i of"
            " 1 event added to the event set" % rcode
        )

    return rcode, None


# int PAPI_add_named_event(int EventSet, const char *EventName);
@papi_error
def add_named_event(eventSet, eventName):
    """Add an event by name to a PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param str eventName: Name of a defined event

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiInitializationError: The PAPI library has not been initialized.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    :raises PapiBugError: Internal error, please send mail to the developers.
    """
    eventName_p = ffi.new("char[]", eventName.encode("ascii"))
    rcode = lib.PAPI_add_named_event(eventSet, eventName_p)

    return rcode, None


# int PAPI_add_events(int EventSet, int *Events, int number);
@papi_error
def add_events(eventSet, eventCodes):
    """Add list of PAPI preset or native hardware events to an event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param list(int) eventCodes: A list of defined events (from :doc:`events`).

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    :raises PapiBugError: Internal error, please send mail to the developers.
    """
    number = len(eventCodes)
    eventCodes_p = ffi.new("int[]", eventCodes)
    rcode = lib.PAPI_add_events(eventSet, eventCodes_p, number)

    if rcode > 0:
        raise PapiError(
            message="Unable to add some of the given events: %i of"
            " %i events added to the event set" % (rcode, number)
        )

    return rcode, None


# int PAPI_assign_eventset_component(int EventSet, int cidx);
@papi_error
def assign_eventset_component(eventSet, component):
    """Assign a component index to an existing but empty eventset.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int component: An integer identifier for a component.
        By convention, component 0 is always the cpu component.


    :raises PapiNoComponentError: The argument component is not a valid component.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rcode = lib.PAPI_assign_eventset_component(eventSet, component)

    return rcode, None


# int PAPI_attach(int EventSet, unsigned long tid);
@papi_error
def attach(eventSet, pid):
    """Attach specified event set to a specific process or thread id.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int pid: A process id.

    :raises PapiComponentError: This feature is unsupported on this component.
    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    """
    rcode = lib.PAPI_attach(eventSet, pid)
    return rcode, None


# int PAPI_cleanup_eventset(int EventSet);
@papi_error
def cleanup_eventset(eventSet):
    """Remove all PAPI events from an event set  and turns off profiling and
    overflow for all events in the EventSet. This can not be called if the
    EventSet is not stopped.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiBugError: Internal error, please send mail to the developers.

    .. WARNING::

        If the user has set profile on an event with the call, then when
        destroying the EventSet the memory allocated by will not be freed. The
        user should turn off profiling on the Events before destroying the
        EventSet to prevent this behavior.
    """
    rcode = lib.PAPI_cleanup_eventset(eventSet)
    return rcode, None


# int PAPI_create_eventset(int *EventSet);
@papi_error
def create_eventset():
    """Create a new empty PAPI event set. The user may then add hardware events to
    the event set by calling :py:func:`add_event` or similar routines.

    :returns: the event set handle.
    :rtype: int

    :raises PapiInvalidValueError: The argument handle has not been initialized
        to PAPI_NULL or the argument is a NULL pointer.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.

    .. NOTE::

        PAPI-C uses a late binding model to bind EventSets to components. When
        an EventSet is first created it is not bound to a component. This will
        cause some API calls that modify EventSet options to fail. An EventSet
        can be bound to a component explicitly by calling
        :py:func:`assign_eventset_component` or implicitly by calling
        :py:func:`add_event` or similar routines.
    """
    eventSet = ffi.new("int*", PAPI_NULL)
    rcode = lib.PAPI_create_eventset(eventSet)
    return rcode, ffi.unpack(eventSet, 1)[0]


# int PAPI_detach(int EventSet);
@papi_error
def detach(eventSet):
    """Detach specified event set from a previously specified process or
    thread id.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiComponentError: This feature is unsupported on this component.
    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    """
    rcode = lib.PAPI_detach(eventSet)
    return rcode, None


# int PAPI_destroy_eventset(int *EventSet);
@papi_error
def destroy_eventset(eventSet):
    """Deallocates memory associated with an empty PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
        Attempting to destroy a non-empty event set or passing in a null
        pointer to be destroyed.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiBugError: Internal error, please send mail to the developers.

    .. WARNING::

        If the user has set profile on an event with the call, then when
        destroying the EventSet the memory allocated by will not be freed. The
        user should turn off profiling on the Events before destroying the
        EventSet to prevent this behavior.
    """
    eventSet_p = ffi.new("int*", eventSet)
    rcode = lib.PAPI_destroy_eventset(eventSet_p)
    return rcode, None


# int PAPI_enum_event(int *EventCode, int modifier);
def enum_event():
    """Enumerate PAPI preset or native events.

    :returns: dictionary of PRESET and NATIVE events.
    :rtype: dict
    """

    return enum_cmp_event(0)


# int PAPI_enum_cmp_event(int *EventCode, int modifier, int cidx)
def enum_cmp_event(component):
    """Enumerate PAPI preset or native events for a given component.

    :param int component: Specifies the component to search in.

    :returns: dictionary of PRESET and NATIVE events.
    :rtype: dict
    """
    events = {"native": [], "preset": []}

    eventCode_p = ffi.new("int*", 0 | PAPI_NATIVE_MASK)
    rcode = lib.PAPI_enum_cmp_event(eventCode_p, 1, component)
    if rcode == 0:
        info = get_event_info(ffi.unpack(eventCode_p, 1)[0])
        events["native"].append(info)
        while lib.PAPI_enum_cmp_event(eventCode_p, 0, component) == 0:
            info = get_event_info(ffi.unpack(eventCode_p, 1)[0])
            events["native"].append(info)

    eventCode_p = ffi.new("int*", 0 | PAPI_PRESET_MASK)
    rcode = lib.PAPI_enum_cmp_event(eventCode_p, 1, component)
    if rcode == 0:
        info = get_event_info(ffi.unpack(eventCode_p, 1)[0])
        events["preset"].append(info)
        while lib.PAPI_enum_cmp_event(eventCode_p, 0, component) == 0:
            info = get_event_info(ffi.unpack(eventCode_p, 1)[0])
            events["preset"].append(info)

    return events


# int PAPI_event_code_to_name(int EventCode, char *out); /**< translate an integer PAPI event code into an ASCII PAPI preset or native name */
@papi_error
def event_code_to_name(eventCode):
    """Convert a numeric hardware event code to a name.

    :param int eventCode: The numeric code for the event.

    :returns: the event name
    :rtype: str

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNotPresetError: The hardware event specified is not a valid PAPI preset.
    :raises PapiNoEventError: The hardware event is not available on the underlying hardware.
    """
    out_p = ffi.new(f"char[{PAPI_MAX_STR_LEN}]")
    rcode = lib.PAPI_event_code_to_name(eventCode, out_p)
    return rcode, ffi.string(out_p, PAPI_MAX_STR_LEN).decode("ascii")


# int PAPI_event_name_to_code(const char *in, int *out);
@papi_error
def event_name_to_code(eventName):
    """Convert a name to a numeric hardware event code.

    :param str eventName: A string containing the event name as listed in
        PAPI_presets or discussed in PAPI_native.

    :returns: the event code.
    :rtype: int

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNotPresetError: The hardware event specified is not a valid PAPI preset.
    :raises PapiInitializationError: The PAPI library has not been initialized.
    :raises PapiNoEventError: The hardware event is not available on the underlying hardware.
    """
    eventName_p = ffi.new("char[]", eventName.encode())
    eventCode_p = ffi.new("int *", PAPI_NULL)
    rcode = lib.PAPI_event_name_to_code(eventName_p, eventCode_p)
    return rcode, ffi.unpack(eventCode_p, 1)[0]


# int PAPI_get_dmem_info(PAPI_dmem_info_t *dest);
@papi_error
def get_dmem_info():
    """Get information about the dynamic memory usage of the current program.

    :returns: dynamic memory usage information
    :rtype: DMEM_info

    :raises PapiComponentError: The function is not implemented for the current component.
    :raises PapiInvalidValueError: Any value in the structure or array may be undefined as indicated by this error value.
    :raises PapiSystemError: A system error occurred.
    """
    info_p = DMEM_info.alloc_empty()
    rcode = lib.PAPI_get_dmem_info(info_p)

    return rcode, DMEM_info(info_p)


# int PAPI_get_event_info(int EventCode, PAPI_event_info_t * info);
@papi_error
def get_event_info(eventCode):
    """Get the event's name and description info.

    :param int eventCode: event code (preset or native).

    :returns: event information
    :rtype: EVENT_info

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNotPresetError: The PAPI preset mask was set,
        but the hardware event specified is not a valid PAPI preset.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying hardware.
        This function fills the event information into a structure.
        In Fortran, some fields of the structure are returned explicitly.
        This function works with existing PAPI preset and native event codes.
    """
    info_p = EVENT_info.alloc_empty()
    rcode = lib.PAPI_get_event_info(eventCode, info_p)

    return rcode, EVENT_info(info_p)


# const PAPI_exe_info_t *PAPI_get_executable_info(void);
def get_executable_info():
    """Get the executable's address space info.

    :returns: executable information
    :rtype: EXECUTABLE_info

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    """
    info_p = lib.PAPI_get_executable_info()

    return None if info_p == ffi.NULL else EXECUTABLE_info(info_p)


# const PAPI_hw_info_t *PAPI_get_hardware_info(void);
def get_hardware_info():
    """Get information about the system hardware.
    In C, this function returns a pointer to a structure containing information about
    the hardware on which the program runs.
    In Fortran, the values of the structure are returned explicitly.

    :returns: hardware information
    :rtype: HARDWARE_info

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    """
    info_p = lib.PAPI_get_hardware_info()

    return None if info_p == ffi.NULL else HARDWARE_info(info_p)


# const PAPI_component_info_t *PAPI_get_component_info(int cidx);
def get_component_info(component):
    """Get information about a specific software component.

    :returns: component information
    :rtype: COMPONENT_info
    """
    info_p = lib.PAPI_get_component_info(component)

    return None if info_p == ffi.NULL else COMPONENT_info(info_p)


# int PAPI_get_multiplex(int EventSet);
def get_multiplex(enventSet):
    return lib.get_multiplex(enventSet)


# int PAPI_get_opt(int option, PAPI_option_t * ptr);

# int PAPI_get_cmp_opt(int option, PAPI_option_t * ptr,int cidx);


# long long PAPI_get_real_cyc(void);
def get_real_cyc():
    """Get real time counter value in clock cycles. Returns the total real
    time passed since some arbitrary starting point. The time is returned in
    clock cycles. This call is equivalent to wall clock time.

    :returns: total real time passed since some arbitrary starting point
    :rtype: ctypes.c_longlong
    """
    return c_longlong(lib.PAPI_get_real_cyc())


# long long PAPI_get_real_nsec(void);
def get_real_nsec():
    """Returns total number of nanoseconds since some arbitrary starting point.

    :rtype: ctypes.c_longlong
    """
    return c_longlong(lib.PAPI_get_real_nsec())


# long long PAPI_get_real_usec(void);
def get_real_usec():
    """Get real time counter value in microseconds. This function returns
    the total real time passed since some arbitrary starting point.
    The time is returned in microseconds. This call is equivalent
    to wall clock time.

    :returns: total real time passed since some arbitrary starting point
    :rtype: ctypes.c_longlong
    """
    return c_longlong(lib.PAPI_get_real_usec())


# const PAPI_shlib_info_t *PAPI_get_shared_lib_info(void);
def get_shared_lib_info():
    """Get address info about the shared libraries used by the process.
    In C, this function returns a pointer to a structure containing
    information about the shared library used by the program.
    There is no Fortran equivalent call.

    :returns: shared libraries information
    :rtype: SHARED_LIB_info
    """
    info_p = lib.PAPI_get_shared_lib_info()

    return None if info_p == ffi.NULL else SHARED_LIB_info(info_p)


# int PAPI_get_thr_specific(int tag, void **ptr); /**< return a pointer to a thread specific stored data structure */
# int PAPI_get_overflow_event_index(int Eventset, long long overflow_vector, int *array, int *number); /**< # decomposes an overflow_vector into an event index array */


# long long PAPI_get_virt_cyc(void);
def get_virt_cyc():
    """Get virtual time counter value in clock cycles

    :returns: virtual time counter value in clock cycles
    :rtype: ctypes.c_longlong
    """
    return c_longlong(lib.PAPI_get_virt_cyc())


# long long PAPI_get_virt_nsec(void);
def get_virt_nsec():
    """Get virtual time counter values in nanoseconds.

    :returns: virtual time counter value in nanoseconds
    :rtype: c_longlong
    """
    return c_longlong(lib.PAPI_get_virt_nsec())


# long long PAPI_get_virt_usec(void);
def get_virt_usec():
    """Get virtual time counter values in microseconds.

    :returns: virtual time counter value in microseconds
    :rtype: c_longlong
    """
    return c_longlong(lib.PAPI_get_virt_usec())


# int PAPI_is_initialized(void);
def is_initialized():
    """Returns the initialized state of the PAPI library.

    :returns: the initialized state of the PAPI library (one of the
        :ref:`consts_init`).
    :rtype: int
    """
    return lib.PAPI_is_initialized()


# int PAPI_library_init(int version);
@papi_error
def library_init(version=PAPI_VER_CURRENT):
    """Initializes the PAPI library.

    :param int version: upon initialization, PAPI checks the argument against
        the internal value of ``PAPI_VER_CURRENT`` when the library was
        compiled.  This guards against portability problems when updating the
        PAPI shared libraries on your system (optional, default:
        :py:data:`pypapi.consts.PAPI_VER_CURRENT`).

    :raises PapiInvalidValueError: papi.h is different from the version used to
        compile the PAPI library.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    :raises PapiComponentError: This component does not support the underlying
        hardware.
    :raises PapiSystemError: A system or C library call failed inside PAPI.

    .. WARNING::

            If you don't call this before using any of the low level PAPI
            calls, your application could core dump.
    """
    rcode = lib.PAPI_library_init(version)
    return rcode, None


# int PAPI_list_events(int EventSet, int *Events, int *number);
@papi_error
def list_events(eventSet):
    """List the events that are members of an event set

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :returns: the list of events.
    :rtype: list(int)

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    """
    number = ffi.new("int*", 0)

    rcode = lib.PAPI_list_events(eventSet, ffi.NULL, number)

    if rcode < 0:
        return rcode, None

    eventCount = ffi.unpack(number, 1)[0]
    events = ffi.new("int[]", eventCount)

    rcode = lib.PAPI_list_events(eventSet, events, number)

    return rcode, ffi.unpack(events, eventCount)


# int PAPI_list_threads(unsigned long *tids, int *number);
@papi_error
def list_threads():
    """List the registered thread ids.

    ``list_threads()`` returns to the caller a list of all thread IDs known to
    PAPI.  This call assumes an initialized PAPI library

    :returns: the list of threads.
    :rtype: list(ctypes.c_ulonglong)

    :raises PapiInvalidValueError: Internal argument is invalid.
    """
    number = ffi.new("int*", 0)

    rcode = lib.PAPI_list_threads(ffi.NULL, number)

    if rcode < 0:
        return rcode, None

    threadCount = ffi.unpack(number, 1)[0]
    threads = ffi.new("unsigned long[]", threadCount)

    rcode = lib.PAPI_list_threads(threads, number)

    return rcode, ffi.unpack(threads, threadCount)


# int PAPI_lock(int);
@papi_error
def lock(lock):
    """Locks one of two mutex variables defined in papi.h.

    ``lock()`` grabs access to one of the two PAPI mutex variables.
    This function is provided to the user to have a platform independent
    call to a (hopefully) efficiently implemented mutex.

    :param int lock: an integer value specifying one of the two user locks:
        :py:const:`~pypapi.consts.PAPI_USR1_LOCK` or
        :py:const:`~pypapi.consts.PAPI_USR2_LOCK`.

    :returns: There is no return value for this call. Upon return from
        PAPI_lock the current thread has acquired exclusive access to the
        specified PAPI mutex.
    """
    rcode = lib.PAPI_lock(lock)

    return rcode, None


# int PAPI_multiplex_init(void);
@papi_error
def multiplex_init():
    """Initializes multiplex support in the PAPI library.

    ``multiplex_init()`` enables and initializes multiplex support in the
    PAPI library.  Multiplexing allows a user to count more events than total
    physical counters by time sharing the existing counters at some loss in
    precision.  Applications that make no use of multiplexing do not need to
    call this routine.
    """

    rcode = lib.PAPI_multiplex_init()

    return rcode, None


# int PAPI_num_cmp_hwctrs(int cidx);
def num_cmp_hwctrs(component):
    """Returns the number of hardware counters for the specified component.

    ``num_cmp_hwctrs()`` returns the number of counters present in the
    specified component.  By convention, component 0 is always the cpu. On some
    components, especially for CPUs, the value returned is a theoretical
    maximum for estimation purposes only.  It might not be possible to easily
    create an EventSet that contains the full number of events. This can be due
    to a variety of reasons:

    1. CPUs (especially Intel and POWER) have the notion of fixed counters that
       can only measure one thing, usually cycles.

    2. Some CPUs have very explicit rules about which event can run in which
       counter.  In this case it might not be possible to add a wanted event
       even if counters are free.

    3. Some CPUs halve the number of counters available when running with SMT
       (multiple CPU threads) enabled.

    4. Some operating systems "steal" a counter to use for things such as NMI
       Watchdog timers.

    The only sure way to see if events will fit is to attempt adding events to
    an EventSet, and doing something sensible if an error is generated.
    :py:func:`library_init` must be called in order for this function to return
    anything greater than ``0``.

    :param int component: An integer identifier for a component. By convention,
        component 0 is always the cpu component.

    :returns: On success, this function returns a value greater than zero.
            A zero result usually means the library has not been initialized.
    :rtype: int
    """

    return lib.PAPI_num_cmp_hwctrs(component)


# int PAPI_num_events(int EventSet);
@papi_error
def num_events(eventSet):
    """Returns the number of events in an event set.

    ``num_events()`` returns the number of preset and/or native events
    contained in an event set.  The event set should be created by
    create_eventset.

    :param int eventSet: an integer handle for a PAPI event set created by
        create_eventset.

    :returns: On success, this function returns the positive number of events
        in the event set.
    :rtype: int

    :raises PapiInvalidValueError: The event count is zero; only if code is compiled with debug enabled.
    :raises PapiNoEventSetError: The EventSet specified does not exist.
    """
    rcode = lib.PAPI_num_events(eventSet)

    return rcode, rcode


# int PAPI_overflow(int EventSet, int EventCode, int threshold, int flags, PAPI_overflow_handler_t handler);
# void PAPI_perror(const char *msg );
def perror(msg):
    """Produces a string on standard error, describing the last library error.

    :param str msg: Optional message to print before the string describing the
        last error message.  The routine ``perror()`` produces a message on the
        standard error output, describing the last error encountered during a
        call to PAPI.  If s is not ``NULL``, s is printed, followed by a colon
        and a space.  Then the error message and a new-line are printed
    """

    msg_p = ffi.new("char[]", msg.encode("ascii"))
    lib.PAPI_perror(msg_p)

    return None


# int PAPI_profil(void *buf, unsigned bufsiz, caddr_t offset, unsigned scale, int EventSet, int EventCode, int threshold, int flags);


# int PAPI_query_event(int EventCode);
@papi_error
def query_event(eventCode):
    """Query if PAPI event exists.

    :param int eventCode: a defined event such as
        :py:const:`~pypapi.events.PAPI_TOT_INS`.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying hardware.
    """

    rcode = lib.PAPI_query_event(eventCode)

    return rcode, None


# int PAPI_query_named_event(const char *EventName);
def query_named_event(eventName):
    """Query if a named PAPI event exists.

    :param str eventName: a defined event such as
        :py:const:`~pypapi.events.PAPI_TOT_INS`.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventError: The PAPI preset is not available on the
        underlying hardware.
    """

    eventName_p = ffi.new("char[]", eventName.encode("ascii"))
    rcode = lib.PAPI_query_named_event(eventName_p)

    return rcode, None


# int PAPI_read(int EventSet, long long * values);
@papi_error
def read(eventSet):
    """Copies the counters of the indicated event set into the provided array.
    The counters continue counting after the read and are not reseted.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :rtype: list(int)

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see
        the errno variable.
    :raises PapiNoEventSetError: The event set specified does not exist.
    """
    eventCount_p = ffi.new("int*", 0)
    rcode = lib.PAPI_list_events(eventSet, ffi.NULL, eventCount_p)

    if rcode < 0:
        return rcode, None

    eventCount = ffi.unpack(eventCount_p, 1)[0]
    values = ffi.new("long long[]", eventCount)

    rcode = lib.PAPI_read(eventSet, values)

    return rcode, ffi.unpack(values, eventCount)


# int PAPI_read_ts(int EventSet, long long * values, long long *cyc);


# int PAPI_register_thread(void);
@papi_error
def register_thread():
    """Notify PAPI that a thread has 'appeared'.

    :raises PapiNoMemoryError: Space could not be allocated to store the new thread information.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see the errno variable.
    :raises PapiComponentError: Hardware counters for this thread could not be initialized.
    """
    rcode = lib.PAPI_register_thread()

    return rcode, None


# int PAPI_remove_named_event(int EventSet, const char *EventName);
@papi_error
def remove_named_event(eventSet, eventName):
    """Removes a named hardware event from a PAPI event set.

    A hardware event can be either a PAPI Preset or a native hardware event
    code.  For a list of PAPI preset events, see PAPI_presets or run the
    papi_avail utility in the PAPI distribution.  PAPI Presets can be passed to
    :py:func:`query_event` to see if they exist on the underlying
    architecture.  For a list of native events available on the current
    platform, run papi_native_avail in the PAPI distribution.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param str eventName:  defined event such as
        :py:const:`~pypapi.events.PAPI_TOT_INS` or a native event.


    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    """

    name_p = ffi.new("char[]", eventName.encode("ascii"))
    rcode = lib.PAPI_remove_named_event(eventSet, name_p)

    return rcode, None


# int PAPI_remove_event(int EventSet, int EventCode);
@papi_error
def remove_event(eventSet, eventCode):
    """Removes a hardware event from a PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int eventCode: A defined event such as
        :py:const:`~pypapi.events.PAPI_TOT_INS` or a native event. (from
        :doc:`events`).

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    """
    rcode = lib.PAPI_remove_event(eventSet, eventCode)
    return rcode, None


# int PAPI_remove_events(int EventSet, int *Events, int number);
@papi_error
def remove_events(eventSet, eventCodes):
    """Removes an list of hardware events from a PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int eventCodes: A list of defined event (from :doc:`events`).

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    """
    number = len(eventCodes)
    eventCodes_p = ffi.new("int[]", eventCodes)
    rcode = lib.PAPI_remove_events(eventSet, eventCodes_p, number)

    if rcode > 0:
        raise PapiError(
            message="Unable to remove some of the given events: "
            "%i of %i events added to the event set" % (rcode, number)
        )

    return rcode, None


# int PAPI_reset(int EventSet);
@papi_error
def reset(eventSet):
    """Reset the hardware event counts in an event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see the errno variable.
    """
    rcode = lib.PAPI_reset(eventSet)

    return rcode, None


# int PAPI_set_debug(int level);
@papi_error
def set_debug(level):
    """Set the current debug level for error output from PAPI.

    :param int level: one of the constants shown in the table below and defined
        in the consts.py file. The possible debug levels for debugging are:

        * :py:const:`~pypapi.consts.PAPI_QUIET` Do not print anything, just
          return the error code
        * :py:const:`~pypapi.consts.PAPI_VERB_ECONT` Print error message and
          continue
        * :py:const:`~pypapi.consts.PAPI_VERB_ESTOP` Print error message and
          exit

    :raises PapiInvalidValueError: The debug level is invalid. The current debug level is used by both the internal error and debug message handler subroutines.
    """

    rcode = lib.PAPI_set_debug(level)
    return rcode, None


# int PAPI_set_cmp_domain(int domain, int cidx);
@papi_error
def set_cmp_domain(domain, component):
    """Set the default counting domain for new event sets bound to the
    specified component.

    Sets the default counting domain for all new event sets in all threads, and
    requires an explicit component argument.  Event sets that are already in
    existence are not affected. To change the domain of an existing event set,
    please see :py:func:`set_opt`.  The reader should note that the domain of
    an event set affects only the mode in which the counter continues to run.
    Counts are still aggregated for the current process, and not for any other
    processes in the system. Thus when requesting
    :py:const:`~pypapi.consts.PAPI_DOM_KERNEL`, the user is asking for events
    that occur on behalf of the process, inside the kernel.

    :param int domain: one of the following constants as defined in
        :doc:`consts`:

        * :py:const:`~pypapi.consts.PAPI_DOM_USER` User context counted
        * :py:const:`~pypapi.consts.PAPI_DOM_KERNEL` Kernel/OS context counted
        * :py:const:`~pypapi.consts.PAPI_DOM_OTHER` Exception/transient mode
          counted
        * :py:const:`~pypapi.consts.PAPI_DOM_SUPERVISOR` Supervisor/hypervisor
          context counted
        * :py:const:`~pypapi.consts.PAPI_DOM_ALL` All above contexts counted
        * :py:const:`~pypapi.consts.PAPI_DOM_MIN` The smallest available
          context
        * :py:const:`~pypapi.consts.PAPI_DOM_MAX` The largest available context
        * :py:const:`~pypapi.consts.PAPI_DOM_HWSPEC` Something other than CPU
          like stuff.

        Individual components can decode low order bits for more meaning.

    :param int component: An integer identifier for a component.
        By convention, component 0 is always the cpu component.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoComponentError:  The argument component is not a valid component.
    """
    rcode = lib.PAPI_set_cmp_domain(domain, component)

    return rcode, None


# int PAPI_set_domain(int domain);
@papi_error
def set_domain(domain):
    """Set the default counting domain for new event sets bound to the cpu
    component.

    Sets the default counting domain for all new event sets created by
    :py:func:`create_eventset` in all threads.  This call implicitly sets the
    domain for the cpu component (component 0) and is included to preserve
    backward compatibility.

    :param int domain: one of the following constants as defined in
        :doc:`consts`:

        * :py:const:`~pypapi.consts.PAPI_DOM_USER` User context counted
        * :py:const:`~pypapi.consts.PAPI_DOM_KERNEL` Kernel/OS context counted
        * :py:const:`~pypapi.consts.PAPI_DOM_OTHER` Exception/transient mode
          counted
        * :py:const:`~pypapi.consts.PAPI_DOM_SUPERVISOR` Supervisor/hypervisor
          context counted
        * :py:const:`~pypapi.consts.PAPI_DOM_ALL` All above contexts counted
        * :py:const:`~pypapi.consts.PAPI_DOM_MAX` The largest available context

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    """

    rcode = lib.PAPI_set_domain(domain)

    return rcode, None


# int PAPI_set_cmp_granularity(int granularity, int cidx);
@papi_error
def set_cmp_granularity(granularity, component):
    """Sets the default counting granularity for eventsets bound to the
    specified component.

    Sets the default counting granularity for all new event sets, and requires
    an explicit component argument.  Event sets that are already in existence
    are not affected.  To change the granularity of an existing event set,
    please see :py:func:`set_opt`.  The reader should note that the granularity of an
    event set affects only the mode in which the counter continues to run.

    :param int granularity: one of the following constants as defined in
        :doc:`consts`:

        * :py:const:`~pypapi.consts.PAPI_GRN_THR` Count each individual thread
        * :py:const:`~pypapi.consts.PAPI_GRN_PROC` Count each individual
          process
        * :py:const:`~pypapi.consts.PAPI_GRN_PROCG` Count each individual
          process group
        * :py:const:`~pypapi.consts.PAPI_GRN_SYS` Count the current CPU
        * :py:const:`~pypapi.consts.PAPI_GRN_SYS_CPU` Count all CPUs
          individually
        * :py:const:`~pypapi.consts.PAPI_GRN_MIN` The finest available
          granularity
        * :py:const:`~pypapi.consts.PAPI_GRN_MAX` The coarsest available
          granularity

    :param int component: An integer identifier for a component.
        By convention, component 0 is always the cpu component.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoComponentError:  The argument component is not a valid component.
    """

    rcode = lib.PAPI_set_cmp_granularity(granularity, component)

    return rcode, None


# int PAPI_set_granularity(int granularity);
@papi_error
def set_granularity(granularity):
    """Sets the default counting granularity for eventsets bound to the cpu
    component.

    Sets the default counting granularity for all new event sets created by
    create_eventset.  This call implicitly sets the granularity for the cpu
    component (component 0) and is included to preserve backward compatibility.

    :param int granularity: one of the following constants as defined in
        :doc:`consts`:

        * :py:const:`~pypapi.consts.PAPI_GRN_THR` Count each individual thread
        * :py:const:`~pypapi.consts.PAPI_GRN_PROC` Count each individual
          process
        * :py:const:`~pypapi.consts.PAPI_GRN_PROCG` Count each individual
          process group
        * :py:const:`~pypapi.consts.PAPI_GRN_SYS` Count the current CPU
        * :py:const:`~pypapi.consts.PAPI_GRN_SYS_CPU` Count all CPUs
          individually
        * :py:const:`~pypapi.consts.PAPI_GRN_MIN` The finest available
          granularity
        * :py:const:`~pypapi.consts.PAPI_GRN_MAX` The coarsest available
          granularity

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    """

    rcode = lib.PAPI_set_granularity(granularity)

    return rcode, None


# int PAPI_set_multiplex(int EventSet);
@papi_error
def set_multiplex(eventSet):
    """Converts a standard event set to a multiplexed event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiInvalidValueError: One or more of the arguments is invalid, or the EventSet is already multiplexed.
    :raises PapiNoComponentError: The EventSet specified is not yet bound to a component.
    :raises PapiNoEventSetError: The EventSet specified does not exist.
    :raises PapiIsRunningError: The EventSet is currently counting events.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rcode = lib.PAPI_set_multiplex(eventSet)
    return rcode, None


# int PAPI_set_opt(int option, PAPI_option_t * ptr);
def set_opt(*args):
    """
    .. WARNING::

        Not implemented in the Python bindings. Will raise ``NotImplementedError``.
    """
    # XXX Function defined for doc reference.
    raise NotImplementedError()  # TODO


# int PAPI_set_thr_specific(int tag, void *ptr);


# void PAPI_shutdown(void);
def shutdown():
    """Finishes using PAPI and free all related resources."""
    lib.PAPI_shutdown()
    return None


# int PAPI_sprofil(PAPI_sprofil_t * prof, int profcnt, int EventSet, int EventCode, int threshold, int flags);


# int PAPI_start(int EventSet);
@papi_error
def start(eventSet):
    """Starts counting all of the hardware events contained in the EventSet. All
    counters are implicitly set to zero before counting.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see
        the errno variable.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiIsRunningError: The event set is currently counting events.
    :raises PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raises PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    """
    rcode = lib.PAPI_start(eventSet)
    return rcode, None


# int PAPI_state(int EventSet, int *status);
@papi_error
def state(eventSet):
    """Returns the counting state of the specified event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :returns: the initialized state of the PAPI library (one of the
        :ref:`consts_state`).
    :rtype: int

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiNoEventSetError: The event set specified does not exist.
    """
    status = ffi.new("int*", 0)
    rcode = lib.PAPI_state(eventSet, status)
    return rcode, ffi.unpack(status, 1)[0]


# int PAPI_stop(int EventSet, long long * values);
@papi_error
def stop(eventSet):
    """Stops counting hardware events in an event set and return current
    values.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :rtype: list(int)

    :raises PapiInvalidValueError: One or more of the arguments is invalid.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see
        the errno variable.
    :raises PapiNoEventSetError: The event set specified does not exist.
    :raises PapiNotRunningError: The EventSet is currently not running.
    """
    eventCount_p = ffi.new("int*", 0)
    rcode = lib.PAPI_list_events(eventSet, ffi.NULL, eventCount_p)

    if rcode < 0:
        return rcode, None

    eventCount = ffi.unpack(eventCount_p, 1)[0]
    values = ffi.new("long long[]", eventCount)

    rcode = lib.PAPI_stop(eventSet, values)

    return rcode, ffi.unpack(values, eventCount)


# char *PAPI_strerror(int);
def strerror(errCode):
    """Returns a string describing the PAPI error code.

    :returns: Error string. If None is returned, errCode is invalid.
    :rtype: str
    """
    errStr_p = lib.PAPI_strerror(errCode)

    return ffi.string(errStr_p).decode("ascii") if errStr_p != ffi.NULL else None


# unsigned long PAPI_thread_id(void);
@papi_error
def thread_id():
    """Get the thread identifier of the current thread.

    :returns: a valid thread identifier.
    :rtype: ctypes.c_ulonglong

    :raises PapiMiscellaneousError: if there are no threads registered.
    :raises PapiInvalidValueError: if the thread id function returns an error.
    """
    rval = lib.PAPI_thread_id()
    return rval, c_ulonglong(rval)


# int PAPI_thread_init(unsigned long (*id_fn) (void));


# int PAPI_unlock(int);
@papi_error
def unlock(lock):
    """Unlocks one of the mutex variables.

    :param int lock: an integer value specifying one of the two user locks:
            :py:const:`~pypapi.consts.PAPI_USR1_LOCK` or
            :py:const:`~pypapi.consts.PAPI_USR2_LOCK`.

    """
    rcode = lib.PAPI_unlock(lock)

    return rcode, None


# int PAPI_unregister_thread(void);
@papi_error
def unregister_thread():
    """Notify PAPI that a thread has 'disappeared'.

    :raises PapiNoMemoryError: Space could not be allocated to store the new thread information.
    :raises PapiSystemError: A system or C library call failed inside PAPI, see the errno variable.
    :raises PapiComponentError: Hardware counters for this thread could not be initialized.
    """
    rcode = lib.PAPI_unregister_thread()

    return rcode, None


# int PAPI_write(int EventSet, long long * values);
@papi_error
def write(eventSet):
    """Write counter values into counters.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raises PapiNoEventSetError: The EventSet specified does not exist.
    :raises PapiComponentError: write() is not implemented for this architecture.
    :raises PapiSystemError: The EventSet is currently counting events and the
        component could not change the values of the running counters.  write()
        writes the counter values provided in the array values into the event
        set EventSet.  The virtual counters managed by the PAPI library will be
        set to the values provided.  If the event set is running, an attempt
        will be made to write the values to the running counters.  This
        operation is not permitted by all components and may result in a
        run-time error.
    """

    return None, None


# int PAPI_get_event_component(int EventCode);
@papi_error
def get_event_component(eventCode):
    """Return component an event belongs to.

    :param int eventCode: EventCode for which we want to know the component
        index.

    :returns: component index
    :rtype: int

    :raises PapiNoComponentError: component does not exist
    """
    rcode = lib.PAPI_get_event_component(eventCode)

    return rcode, rcode


# int PAPI_get_eventset_component(int EventSet);
@papi_error
def get_eventset_component(eventSet):
    """Returns index for component an EventSet is assigned to.

    :param int eventSet: EventSet for which we want to know the component
        index.

    :returns: component index
    :rtype: int

    :raises PapiNoEventSetError: EventSet does not exist.
    :raises PapiNoComponentError: component is invalid or does not exist
        positive value valid component index.
    """
    rcode = lib.PAPI_get_eventset_component(eventSet)

    return rcode, rcode


# int PAPI_get_component_index(const char *name);
@papi_error
def get_component_index(componentName):
    """Returns the component index for the named component.

    :param int componentName: name of component to find index for

    :returns: component index
    :rtype: int

    :raises PapiNoComponentError: component does not exist
    """
    componentName_p = ffi.new("char[]", componentName.encode("ascii"))
    rcode = lib.PAPI_get_component_index(componentName_p)

    return rcode, rcode


# int PAPI_disable_component(int cidx);
@papi_error
def disable_component(component):
    """Disables the specified component.

    :param int component: component index of component to be disabled

    :returns: component index
    :rtype: int

    :raises PapiNoComponentError: component does not exist
    :raises PapiInitializationError: cannot disable as PAPI has already been
        initialized
    """
    rcode = lib.PAPI_disable_component(component)

    return rcode, None


# int PAPI_disable_component_by_name(const char *name );
@papi_error
def disable_component_by_name(componentName):
    """Disables the named component.

    :param str componentName: name of the component to disable.

    :returns: component index
    :rtype: int

    :raises PapiNoComponentError: component does not exist
    :raises PapiInitializationError: unable to disable the component, the
        library has already been initialized
    """
    componentName_p = ffi.new("char[]", componentName.encode("ascii"))
    rcode = lib.PAPI_disable_component_by_name(componentName_p)

    return rcode, None


# int PAPI_num_components(void);
def num_components():
    """Get the number of components available on the system.

    :returns: Number of components available on the system. Query the library
        for a component count.
    :rtype: int
    """
    return lib.PAPI_num_components()


# int PAPI_flips_rate(int event, float *rtime, float *ptime, long long *flpins, float *mflips);
@papi_error
def flips_rate(event):
    """Simplified call to get Mflips/s (floating point instruction rate), real
    and processor time.

    :param int event: one of the three presets in :doc:`consts`:

        * :py:const:`~pypapi.consts.PAPI_FP_INS`,
        * :py:const:`~pypapi.consts.PAPI_VEC_SP`,
        * :py:const:`~pypapi.consts.PAPI_VEC_DP`

    :rtype: structs.Flips

    :raises PapiInvalidValueError: The counters were already started by
        something other than :py:func:`flips_rate`.
    :raises PapiNoEventError: The floating point operations or total cycles
        event does not exist.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpins = ffi.new("long long*", 0)
    mflips = ffi.new("float*", 0)

    rcode = lib.PAPI_flips_rate(event, rtime, ptime, flpins, mflips)

    return rcode, Flips(
        event,
        ffi.unpack(rtime, 1)[0],
        ffi.unpack(ptime, 1)[0],
        ffi.unpack(flpins, 1)[0],
        ffi.unpack(mflips, 1)[0],
    )


# int PAPI_flops_rate(int event, float *rtime, float *ptime, long long * flpops, float *mflops);
@papi_error
def flops_rate(event):
    """Simplified call to get Mflops/s (floating point operation rate), real
    and processor time.

    :param int event: one of the three presets in :doc:`consts`:

        * :py:const:`~pypapi.consts.PAPI_FP_OPS`,
        * :py:const:`~pypapi.consts.PAPI_SP_OPS`,
        * :py:const:`~pypapi.consts.PAPI_DP_OPS`

    :rtype: structs.Flops

    :raises PapiInvalidValueError: The counters were already started by
        something other than :py:func:`flops_rate`.
    :raises PapiNoEventError: The floating point instructions or total cycles
        event does not exist.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpops = ffi.new("long long*", 0)
    mflops = ffi.new("float*", 0)

    rcode = lib.PAPI_flops_rate(event, rtime, ptime, flpops, mflops)

    return rcode, Flops(
        event,
        ffi.unpack(rtime, 1)[0],
        ffi.unpack(ptime, 1)[0],
        ffi.unpack(flpops, 1)[0],
        ffi.unpack(mflops, 1)[0],
    )


# int PAPI_ipc(float *rtime, float *ptime, long long *ins, float *ipc);
@papi_error
def ipc():
    """Simplified call to get instructions per cycle, real and processor time.

    :rtype: structs.IPC

    :raises PapiInvalidValueError: The counters were already started by
        something other than :py:func:`ipc`.
    :raises PapiNoEventError: The total instructions or total cycles event does
        not exist.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    ins = ffi.new("long long*", 0)
    ipc_ = ffi.new("float*", 0)

    rcode = lib.PAPI_ipc(rtime, ptime, ins, ipc_)

    return rcode, IPC(
        ffi.unpack(rtime, 1)[0],
        ffi.unpack(ptime, 1)[0],
        ffi.unpack(ins, 1)[0],
        ffi.unpack(ipc_, 1)[0],
    )


# int PAPI_epc(int event, float *rtime, float *ptime, long long *ref,
#              long long *core, long long *evt, float *epc);
@papi_error
def epc(event=0):
    """Simplified call to get arbitrary events per cycle, real and processor
    time.

    :param int event: event code to be measured (from :doc:`events`, default:
        :py:const:`~pypapi.events.PAPI_TOT_INS`).

    :rtype: structs.EPC

    :raises PapiInvalidValueError: The counters were already started by
        something other than :py:func:`epc`.
    :raises PapiNoEventError: The total instructions or total cycles event does
        not exist.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    ref = ffi.new("long long*", 0)
    core = ffi.new("long long*", 0)
    evt = ffi.new("long long*", 0)
    epc_ = ffi.new("float*", 0)

    rcode = lib.PAPI_epc(event, rtime, ptime, ref, core, evt, epc_)

    return rcode, EPC(
        ffi.unpack(rtime, 1)[0],
        ffi.unpack(ptime, 1)[0],
        ffi.unpack(ref, 1)[0],
        ffi.unpack(core, 1)[0],
        ffi.unpack(evt, 1)[0],
        ffi.unpack(epc_, 1)[0],
    )


# int PAPI_rate_stop();
def rate_stop():
    """Stops a running event set of a rate function.

    :raises PapiNoEventError: The EventSet is not started yet.
    :raises PapiNoMemoryError: Insufficient memory to complete the operation.
    """
    rcode = lib.PAPI_rate_stop()

    return rcode, None
