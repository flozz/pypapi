from collections import namedtuple

import numpy as np

from ._papi import ffi


class PAPI_Base:
    fields = {}
    s_fields = {}

    def __init__(self, cdata):
        for field, f_type in self.fields.items():
            setattr(self, field, self.cdata_to_python(getattr(cdata, field), f_type))
        for field, f_tuple in self.s_fields.items():
            setattr(
                self,
                field,
                self.special_cdata_to_python(
                    getattr(cdata, field), f_tuple[1], f_tuple[0]
                ),
            )

    def __repr__(self):
        attr = [f"\t{field}={getattr(self, field)}\n" for field in self.fields]
        s_attr = [f"\t{field}={getattr(self, field)}\n" for field in self.s_fields]
        return f"{self.__class__.__name__}(\n{''.join(attr+s_attr)})"

    @staticmethod
    def cdata_to_python(cdata, data_type):
        split = data_type.index(":")
        data_type, nested_type = data_type[:split], data_type[split + 1 :]

        if data_type == "num":
            if nested_type == "intc":
                return np.uintc(cdata).astype(np.intc)
            return getattr(np, nested_type)(cdata)
        if data_type == "str":
            return ffi.string(cdata).decode("ascii") if cdata != ffi.NULL else None
        if data_type == "arr":
            return [
                PAPI_Base.cdata_to_python(nested_cdata, nested_type)
                for nested_cdata in cdata
            ]
        return None

    def special_cdata_to_python(self, cdata, level, data_type):
        if isinstance(level, str):  # dynamic array
            return [data_type(cdata[i]) for i in range(getattr(self, level))]
        if level == 0:
            return data_type(cdata)

        return [
            self.special_cdata_to_python(nested_cdata, level - 1, data_type)
            for nested_cdata in cdata
        ]


class DMEM_info(PAPI_Base):
    fields = {
        "peak": "num:longlong",
        "size": "num:longlong",
        "resident": "num:longlong",
        "high_water_mark": "num:longlong",
        "shared": "num:longlong",
        "text": "num:longlong",
        "library": "num:longlong",
        "heap": "num:longlong",
        "locked": "num:longlong",
        "stack": "num:longlong",
        "pagesize": "num:longlong",
        "pte": "num:longlong",
    }

    @classmethod
    def alloc_empty(cls):
        return ffi.new("PAPI_dmem_info_t *")


class EVENT_info(PAPI_Base):
    fields = {
        "event_code": "num:intc",
        "symbol": "str:",
        "short_descr": "str:",
        "long_descr": "str:",
        "component_index": "num:intc",
        "units": "str:",
        "location": "num:intc",
        "data_type": "num:intc",
        "value_type": "num:intc",
        "timescope": "num:intc",
        "update_type": "num:intc",
        "update_freq": "num:intc",
        "count": "num:uintc",
        "event_type": "num:uintc",
        "derived": "str:",
        "postfix": "str:",
        "code": "arr:num:uintc",
        "name": "arr:str:",
        "note": "str:",
    }

    @classmethod
    def alloc_empty(cls):
        return ffi.new("PAPI_event_info_t *")


class MH_tlb(PAPI_Base):
    fields = {
        "type": "num:intc",
        "num_entries": "num:intc",
        "page_size": "num:intc",
        "associativity": "num:intc",
    }


class MH_cache(PAPI_Base):
    fields = {
        "type": "num:intc",
        "size": "num:intc",
        "line_size": "num:intc",
        "num_lines": "num:intc",
        "associativity": "num:intc",
    }


class MH_level(PAPI_Base):
    s_fields = {"tlb": (MH_tlb, 1), "cache": (MH_cache, 1)}


class MH_info(PAPI_Base):
    fields = {"levels": "num:intc"}

    s_fields = {"level": (MH_level, 1)}


class HARDWARE_info(PAPI_Base):
    fields = {
        "ncpu": "num:intc",
        "threads": "num:intc",
        "cores": "num:intc",
        "sockets": "num:intc",
        "nnodes": "num:intc",
        "totalcpus": "num:intc",
        "vendor": "num:intc",
        "vendor_string": "str:",
        "model": "num:intc",
        "model_string": "str:",
        "revision": "num:single",
        "cpuid_family": "num:intc",
        "cpuid_model": "num:intc",
        "cpuid_stepping": "num:intc",
        "cpu_max_mhz": "num:intc",
        "cpu_min_mhz": "num:intc",
        "virtualized": "num:intc",
        "virtual_vendor_string": "str:",
        "virtual_vendor_version": "str:",
    }

    s_field = {"mem_hierarchy": (MH_info, 1)}


class ADDR_p(PAPI_Base):
    def __init__(self, cdata):
        if cdata == ffi.NULL:
            self.addr = None
        else:
            self.addr = int(cdata.__repr__().split()[-1].strip()[:-1], base=16)

    def __repr__(self):
        return f"ADDR_p(addr={hex(self.addr) if self.addr is not None else 'NULL'})"


class ADDR_map(PAPI_Base):
    fields = {"name": "str:"}
    s_fields = {
        "text_start": (ADDR_p, 0),
        "text_end": (ADDR_p, 0),
        "data_start": (ADDR_p, 0),
        "data_end": (ADDR_p, 0),
        "bss_start": (ADDR_p, 0),
        "bss_end": (ADDR_p, 0),
    }


class EXECUTABLE_info(PAPI_Base):
    fields = {
        "fullname": "str:",
    }

    s_field = {"address_info": (ADDR_map, 0)}


class COMPONENT_info(PAPI_Base):
    fields = {
        "name": "str:",
        "short_name": "str:",
        "description": "str:",
        "version": "str:",
        "support_version": "str:",
        "kernel_version": "str:",
        "disabled_reason": "str:",
        "disabled": "num:intc",
        "CmpIdx": "num:intc",
        "num_cntrs": "num:intc",
        "num_mpx_cntrs": "num:intc",
        "num_preset_events": "num:intc",
        "num_native_events": "num:intc",
        "default_domain": "num:intc",
        "available_domains": "num:intc",
        "default_granularity": "num:intc",
        "available_granularities": "num:intc",
        "hardware_intr_sig": "num:intc",
        "component_type": "num:intc",
        "pmu_names": "arr:str:",
        "reserved": "arr:num:uintc",
        "hardware_intr": "num:uintc",
        "precise_intr": "num:uintc",
        "posix1b_timers": "num:uintc",
        "kernel_profile": "num:uintc",
        "kernel_multiplex": "num:uintc",
        "fast_counter_read": "num:uintc",
        "fast_real_timer": "num:uintc",
        "fast_virtual_timer": "num:uintc",
        "attach": "num:uintc",
        "attach_must_ptrace": "num:uintc",
        "cntr_umasks": "num:uintc",
        "cpu": "num:uintc",
        "inherit": "num:uintc",
        "reserved_bits": "num:uintc",
    }


class SHARED_LIB_info(PAPI_Base):
    fields = {
        "count": "num:intc",
    }

    s_fields = {"map": (ADDR_map, "count")}


Flips = namedtuple("Flips", "event rtime ptime flpins mflips")

Flops = namedtuple("Flops", "event rtime ptime flpops mflops")

IPC = namedtuple("IPC", "rtime ptime ins ipc")

EPC = namedtuple("EPC", "rtime ptime ref core evt epc")
