Installing PyPAPI
=================

As PAPI is a C library, it must be compiled. On Ubuntu / Debian, you can
install the ``build-essential`` package.


From PYPI
---------

TODO: Not yet available on PYPI


From Source
-----------

First clone the project's repository and go into it:

::

    git clone https://github.com/flozz/pypapi.git
    cd pypapi

Then initialize and update git sub-modules:

::

    git submodule init
    git submodule update

Finally, execute the following command:

::

    python setup.py install

.. note::

    you may require root permission if you want to install the package
    system-wild.


