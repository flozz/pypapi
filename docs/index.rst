Welcome to PyPAPI's documentation!
==================================

PyPAPI is a Python binding for the PAPI (Performance Application Programming
Interface) library. PyPAPI implements the whole PAPI High Level API and
partially the Low Level API.

Example usage:
--------------

::

    # High Level API

    from pypapi import papi_high

    papi_high.hl_region_begin("computation")

    # computation

    papi_high.hl_region_end("computation")


::

    # Low Level API

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


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   papi_high
   papi_low
   structs
   events
   consts
   exceptions
   licenses

* :ref:`genindex`
* :ref:`modindex`

* `Github <https://github.com/flozz/pypapi>`_
