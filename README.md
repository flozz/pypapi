# PyPAPI

PyPAPI is a Python binding for the [PAPI (Performance Application Programming
Interface) library][libpapi] (only the high level api).

**CURRENTLY, THIS IS ONLY A QUICK AND DIRTY TEST, DO NOT USE IN PRODUCTION!**

## Installing PyPAPI

As PAPI is a C library, it must be compiled. On Ubuntu / Debian, you can
install the `build-essential` package.

### From Source

First clone the project's repository and go into it:

    git clone https://github.com/flozz/pypapi.git
    cd pypapi

Then initialize and update git sub-modules:

    git submodule init
    git submodule update

Finally, execute the following command:

    python setup.py install

__NOTE:__ you may require root permission if you want to install the package
system-wild.

[libpapi]: http://icl.cs.utk.edu/papi/index.html
