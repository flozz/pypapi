from collections import namedtuple


NumCounters = int
Flips = namedtuple("Flips", "rcode rtime ptime flpins mflips")
Flops = namedtuple("Flops", "rcode rtime ptime flpops mflops")
IPC = namedtuple("IPC", "rcode rtime ptime ins ipc")
EPC = namedtuple("EPC", "rcode rtime ptime ref core evt epc")
