import os

from cffi import FFI


_ROOT = os.path.abspath(os.path.dirname(__file__))
_PAPI_H = os.path.join(_ROOT, "papi.h")


ffibuilder = FFI()
ffibuilder.set_source(
    "pypapi._papi",
    '#include "papi.h"',
    extra_objects=[os.path.join(_ROOT, "..", "papi", "src", "libpapi.a")],
    include_dirs=[_ROOT],
)
ffibuilder.cdef(open(_PAPI_H, "r").read())


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
