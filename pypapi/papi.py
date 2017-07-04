from collections import namedtuple

from ._papi import lib, ffi


# TODO (high api):
# [ ] accum_counters
# [ ] epc
# [x] flips
# [x] flops
# [ ] ipc
# [ ] num_components
# [ ] num_counters
# [ ] read_counters
# [ ] start_counters
# [ ] stop_counters


_Flips = namedtuple("Flips", "rvalue rtime ptime flpins mflips")

def flips():
    """Simplified call to get Mflips/s (floating point instruction rate), real
    and processor time.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpins = ffi.new("long long*", 0)
    mflips = ffi.new("float*", 0)

    rvalue = lib.PAPI_flops(rtime, ptime, flpins, mflips)

    return _Flips(
            rvalue,
            ffi.unpack(rtime, 1)[0],
            ffi.unpack(ptime, 1)[0],
            ffi.unpack(flpins, 1)[0],
            ffi.unpack(mflips, 1)[0]
            )


_Flops = namedtuple("Flops", "rvalue rtime ptime flpops mflops")

def flops():
    """Simplified call to get Mflops/s (floating point operation rate), real
    and processor time.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpops = ffi.new("long long*", 0)
    mflops = ffi.new("float*", 0)

    rvalue = lib.PAPI_flops(rtime, ptime, flpops, mflops)

    return _Flops(
            rvalue,
            ffi.unpack(rtime, 1)[0],
            ffi.unpack(ptime, 1)[0],
            ffi.unpack(flpops, 1)[0],
            ffi.unpack(mflops, 1)[0]
            )
