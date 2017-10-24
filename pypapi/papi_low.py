"""
TODO
"""


from ._papi import lib, ffi
from .exceptions import papi_error


# int PAPI_add_event(int EventSet, int Event);
@papi_error
def add_event(eventSet, eventCode):
    """add_event(eventSet, eventCode)

    Add single PAPI preset or native hardware event to an event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int eventCode: A defined event such as ``PAPI_TOT_INS`` (from
        :doc:`events`).

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoMemoryError: Insufficient memory to complete the operation.
    :raise PapiNoEventSetError: The event set specified does not exist.
    :raise PapiIsRunningError: The event set is currently counting events.
    :raise PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raise PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    :raise PapiBugError: Internal error, please send mail to the developers.
    """
    pass  # TODO


# int PAPI_add_events(int EventSet, int *Events, int number);
@papi_error
def add_events(eventSet, eventCodes):
    """add_events(eventSet, eventCodes)

    Add list of PAPI preset or native hardware events to an event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param list(int) eventCodes: A list of defined events (from :doc:`events`).

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoMemoryError: Insufficient memory to complete the operation.
    :raise PapiNoEventSetError: The event set specified does not exist.
    :raise PapiIsRunningError: The event set is currently counting events.
    :raise PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raise PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    :raise PapiBugError: Internal error, please send mail to the developers.
    """
    pass  # TODO


# int PAPI_cleanup_eventset(int EventSet);
@papi_error
def cleanup_eventset(eventSet):
    """cleanup_eventset(eventSet)

    Remove all PAPI events from an event set  and turns off profiling and
    overflow for all events in the EventSet. This can not be called if the
    EventSet is not stopped.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoEventSetError: The event set specified does not exist.
    :raise PapiIsRunningError: The event set is currently counting events.
    :raise PapiBugError: Internal error, please send mail to the developers.

    .. WARNING::

        If the user has set profile on an event with the call, then when
        destroying the EventSet the memory allocated by will not be freed. The
        user should turn off profiling on the Events before destroying the
        EventSet to prevent this behavior.
    """
    pass  # TODO


# int PAPI_create_eventset(int *EventSet);
@papi_error
def create_eventset():
    """create_eventset()

    Create a new empty PAPI event set. The user may then add hardware events to
    the event set by calling :py:func:`add_event` or similar routines.

    :returns: the event set handle.
    :rtype: int

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoMemoryError: Insufficient memory to complete the operation.

    .. NOTE::

        PAPI-C uses a late binding model to bind EventSets to components. When
        an EventSet is first created it is not bound to a component. This will
        cause some API calls that modify EventSet options to fail. An EventSet
        can be bound to a component explicitly by calling
        :py:func:`assign_eventset_component` or implicitly by calling
        :py:func:`add_event` or similar routines.
    """
    pass  # TODO


# int PAPI_destroy_eventset(int *EventSet);
@papi_error
def destroy_eventset(eventSet):
    """destroy_eventset(eventSet)

    Deallocates memory associated with an empty PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoEventSetError: The event set specified does not exist.
    :raise PapiIsRunningError: The event set is currently counting events.
    :raise PapiBugError: Internal error, please send mail to the developers.

    .. WARNING::

        If the user has set profile on an event with the call, then when
        destroying the EventSet the memory allocated by will not be freed. The
        user should turn off profiling on the Events before destroying the
        EventSet to prevent this behavior.
    """
    pass  # TODO  /!\ pointer param /!\


# int PAPI_list_events(int EventSet, int *Events, int *number);
@papi_error
def list_events(eventSet):
    """list_events(eventSet)

    List the events that are members of an event set

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.

    :returns: the list of events.
    :rtype: list(int)

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoEventSetError: The event set specified does not exist.
    """
    pass  # TODO


# int PAPI_remove_event(int EventSet, int EventCode);
@papi_error
def remove_event(eventSet, eventCode):
    """remove_event(eventSet, eventCode)

    Remove a hardware event from a PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int eventCode: A defined event such as ``PAPI_TOT_INS`` or a native
        event. (from :doc:`events`).

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoEventSetError: The event set specified does not exist.
    :raise PapiIsRunningError: The event set is currently counting events.
    :raise PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raise PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    """
    pass  # TODO


# int PAPI_remove_events(int EventSet, int *Events, int number);
@papi_error
def remove_events(eventSet, eventCodes):
    """remove_events(eventSet, eventCodes)

    Remove an list of hardware events from a PAPI event set.

    :param int eventSet: An integer handle for a PAPI Event Set as created by
        :py:func:`create_eventset`.
    :param int eventCodes: A list of defined event (from :doc:`events`).

    :raise PapiInvalidValueError: One or more of the arguments is invalid.
    :raise PapiNoEventSetError: The event set specified does not exist.
    :raise PapiIsRunningError: The event set is currently counting events.
    :raise PapiConflictError: The underlying counter hardware can not count
        this event and other events in the event set simultaneously.
    :raise PapiNoEventError: The PAPI preset is not available on the underlying
        hardware.
    """
    pass  # TODO