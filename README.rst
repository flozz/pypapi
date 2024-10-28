PyPAPI
======

|GitHub| |PyPI| |License| |Discord| |Github Actions| |Black|

PyPAPI is a Python binding for the `PAPI (Performance Application Programming
Interface) <http://icl.cs.utk.edu/papi/index.html>`__ library. PyPAPI
implements the whole PAPI High Level API and partially the Low Level API.

.. NOTE::

    Starting with **v5.5.1.4**, PyPAPI is only compatible with GCC 7.0 or
    higher. Please use previous releases for older GCC version.


Documentation:
--------------

* https://flozz.github.io/pypapi/


Installing PyPAPI
-----------------

See this page of the documentation:

* https://flozz.github.io/pypapi/install.html


Hacking
-------

Building PyPAPI For Local Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To work on PyPAPI, you first have to clone this repositiory and
initialize and update submodules::

    git clone https://github.com/flozz/pypapi.git
    cd pypapi

    git submodule init
    git submodule update

Then you have to build both PAPI and the C library inside the ``pypapi``
module. This can be done with the following commands::

    python setup.py build
    python pypapi/papi_build.py


Linting and Code formatting
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build lint the code, you first need to install Nox::

    pip install nox

Then, run the following command::

    nox -s lint

To automatically coding style issues, run::

    nox -s black_fix


Generating Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

To build the Sphinx documentation, you first need to install Nox::

    pip install nox

Then, run the following command::

    nox -s gendoc


Support this project
--------------------

Want to support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__
* `💵️ Give me a tip on PayPal <https://www.paypal.me/0xflozz>`__
* `❤️ Sponsor me on GitHub <https://github.com/sponsors/flozz>`__


Changelog
---------


* **[NEXT]** (changes on ``master``, but not released yet):

  * Nothing yet ;)

* **v6.0.0.2:**

  * misc: Added Python 3.13 support (@flozz)
  * misc!: Removed Python 3.8 support (@flozz)

* **v6.0.0.1:**

  * feat!: Updated the PAPI library to v6.0.0.1 (@SerodioJ, #37)

* **v5.5.1.6:**

  * chore: Added code linting with Flake8 (@flozz)
  * chore: Added code formatter and reformatted all files with Black (@flozz)
  * chore: Added Nox to run code linting, code formatting, doc building tasks (@flozz)
  * chore: Updated dev dependnecies (@flozz)
  * chore: Automatically build and publish sdist package and wheels for Linux (@flozz, #39)
  * docs: Updated documentation (@flozz)

* **v5.5.1.5:**

  * fix: Fixed issue with module named ``types.py`` (@mcopik, #19)

* **v5.5.1.4:**

  * chore: Fixed compilation with GCC 8 and newer (@maresmar, #18)
  * chore!: PyPAPI is no more compatible with GCC < 7.0

* **v5.5.1.3:**

  * chore: Removed ``.o``, ``.lo`` and other generated objects from the package

* **v5.5.1.2:**

  * feat: Partial bindings for the low level API

* **v5.5.1.1:**

  * chore: Added missing files to build PAPI

* **v5.5.1.0:**

  * feat: Initial release (binding for papy 5.5.1)


.. |GitHub| image:: https://img.shields.io/github/stars/flozz/pypapi?label=GitHub&logo=github
   :target: https://github.com/flozz/pypapi

.. |PyPI| image:: https://img.shields.io/pypi/v/python_papi.svg
   :target: https://pypi.python.org/pypi/python_papi

.. |License| image:: https://img.shields.io/github/license/flozz/pypapi
   :target: https://flozz.github.io/pypapi/licenses.html

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |Github Actions| image:: https://github.com/flozz/pypapi/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/pypapi/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable
