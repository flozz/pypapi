Events
======


Bellow the list of all events supported by PAPI. They can be used with the
:py:func:`~pypapi.papi.start_counters` function:

::

    from pypapi import events, start_counters

    start_counters([
        events.PAPI_FP_OPS,
        events.PAPI_TOT_CYC
        ])


Event List
----------

.. automodule:: pypapi.events
    :members:
