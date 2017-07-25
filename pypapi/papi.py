from ._papi import lib, ffi
from .types import Flips, Flops, IPC, EPC
from .exceptions import papi_error


# TODO (high api):
# [ ] accum_counters
# [x] epc
# [x] flips
# [x] flops
# [x] ipc
# [x] num_components
# [x] num_counters
# [ ] read_counters
# [x] start_counters
# [x] stop_counters


def num_counters():
    """Get the number of hardware counters available on the system.
    """
    return lib.PAPI_num_counters()


def num_components():
    """Get the number of components available on the system.
    """
    return lib.PAPI_num_components()


@papi_error
def start_counters(events):
    """Start counting hardware events.
    """
    for i in range(0, len(events)):
        if events[i] | 0x80000000:
            events[i] = events[i] | ~0x7FFFFFFF

    events_ = ffi.new("int[]", events)
    array_len = len(events)

    rcode = lib.PAPI_start_counters(events_, array_len)

    return rcode, None


@papi_error
def stop_counters(array_len=0):
    """Stop counters and return current counts.
    """
    values = ffi.new("long long[]", array_len)

    rcode = lib.PAPI_stop_counters(values, array_len)

    return rcode, ffi.unpack(values, array_len)


@papi_error
def flips():
    """Simplified call to get Mflips/s (floating point instruction rate), real
    and processor time.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpins = ffi.new("long long*", 0)
    mflips = ffi.new("float*", 0)

    rcode = lib.PAPI_flops(rtime, ptime, flpins, mflips)

    return rcode, Flips(
            ffi.unpack(rtime, 1)[0],
            ffi.unpack(ptime, 1)[0],
            ffi.unpack(flpins, 1)[0],
            ffi.unpack(mflips, 1)[0]
            )


@papi_error
def flops():
    """Simplified call to get Mflops/s (floating point operation rate), real
    and processor time.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpops = ffi.new("long long*", 0)
    mflops = ffi.new("float*", 0)

    rcode = lib.PAPI_flops(rtime, ptime, flpops, mflops)

    return rcode, Flops(
            ffi.unpack(rtime, 1)[0],
            ffi.unpack(ptime, 1)[0],
            ffi.unpack(flpops, 1)[0],
            ffi.unpack(mflops, 1)[0]
            )


@papi_error
def ipc():
    """Gets instructions per cycle, real and processor time.
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
            ffi.unpack(ipc_, 1)[0]
            )


@papi_error
def epc(event=0):
    """Gets (named) events per cycle, real and processor time, reference and
    core cycles.
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
            ffi.unpack(epc_, 1)[0]
            )
