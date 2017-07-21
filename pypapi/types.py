from collections import namedtuple


Flips = namedtuple("Flips", "rcode rtime ptime flpins mflips")
Flops = namedtuple("Flops", "rcode rtime ptime flpops mflops")
IPC = namedtuple("IPC", "rcode rtime ptime ins ipc")
