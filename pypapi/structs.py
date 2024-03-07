from collections import namedtuple

import ctypes

from ._papi import ffi


class PAPI_Base:
    """Base class for PAPI structs."""

    fields = {}
    """Fields of the struct (refer to PAPI's documentation for each field's meaning)"""
    s_fields = {}
    """Special Fields of the struct (refer to PAPI's documentation for each field's meaning)"""

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
        return f"{self.__class__.__name__}(\n{''.join(attr + s_attr)})"

    @staticmethod
    def cdata_to_python(cdata, data_type):
        """Converts C data to Python objects."""
        split = data_type.index(":")
        data_type, nested_type = data_type[:split], data_type[split + 1 :]

        if data_type == "num":
            return getattr(ctypes, nested_type)(cdata).value
        if data_type == "str":
            return ffi.string(cdata).decode("ascii") if cdata != ffi.NULL else None
        if data_type == "arr":
            return [
                PAPI_Base.cdata_to_python(nested_cdata, nested_type)
                for nested_cdata in cdata
            ]
        return None

    def special_cdata_to_python(self, cdata, level, data_type):
        """Converts special C data, such as structs, to Python objects."""
        if isinstance(level, str):  # dynamic array
            return [data_type(cdata[i]) for i in range(getattr(self, level))]
        if level == 0:
            return data_type(cdata)

        return [
            self.special_cdata_to_python(nested_cdata, level - 1, data_type)
            for nested_cdata in cdata
        ]


class DMEM_info(PAPI_Base):
    """Dynamic memory usage info class. Maps to PAPI_dmem_info_t data structure."""

    fields = {
        "peak": "num:c_longlong",
        "size": "num:c_longlong",
        "resident": "num:c_longlong",
        "high_water_mark": "num:c_longlong",
        "shared": "num:c_longlong",
        "text": "num:c_longlong",
        "library": "num:c_longlong",
        "heap": "num:c_longlong",
        "locked": "num:c_longlong",
        "stack": "num:c_longlong",
        "pagesize": "num:c_longlong",
        "pte": "num:c_longlong",
    }

    @classmethod
    def alloc_empty(cls):
        """Allocate empty PAPI_dmem_info_t using ffi.new"""
        return ffi.new("PAPI_dmem_info_t *")


class EVENT_info(PAPI_Base):
    """Envent info class. Maps to PAPI_event_info_t data structure."""

    fields = {
        "event_code": "num:c_int",
        "symbol": "str:",
        "short_descr": "str:",
        "long_descr": "str:",
        "component_index": "num:c_int",
        "units": "str:",
        "location": "num:c_int",
        "data_type": "num:c_int",
        "value_type": "num:c_int",
        "timescope": "num:c_int",
        "update_type": "num:c_int",
        "update_freq": "num:c_int",
        "count": "num:c_uint",
        "event_type": "num:c_uint",
        "derived": "str:",
        "postfix": "str:",
        "code": "arr:num:c_uint",
        "name": "arr:str:",
        "note": "str:",
    }

    @classmethod
    def alloc_empty(cls):
        """Allocate empty PAPI_event_info_t using ffi.new"""
        return ffi.new("PAPI_event_info_t *")


class MH_tlb(PAPI_Base):
    """Memory Hierarchy TLB info class. Maps to PAPI_mh_tlb_info_t data structure."""

    fields = {
        "type": "num:c_int",
        "num_entries": "num:c_int",
        "page_size": "num:c_int",
        "associativity": "num:c_int",
    }


class MH_cache(PAPI_Base):
    """Memory Hierarchy Cache info class. Maps to PAPI_mh_cache_info_t data structure."""

    fields = {
        "type": "num:c_int",
        "size": "num:c_int",
        "line_size": "num:c_int",
        "num_lines": "num:c_int",
        "associativity": "num:c_int",
    }


class MH_level(PAPI_Base):
    """Memory Hierarchy Level info class. Maps to PAPI_mh_level_t data structure."""

    s_fields = {"tlb": (MH_tlb, 1), "cache": (MH_cache, 1)}


class MH_info(PAPI_Base):
    """Memory Hierarchy info class. Maps to PAPI_mh_info_t data structure."""

    fields = {"levels": "num:c_int"}

    s_fields = {"level": (MH_level, 1)}


class HARDWARE_info(PAPI_Base):
    """Hardware info class. Maps to PAPI_hw_info_t data structure."""

    fields = {
        "ncpu": "num:c_int",
        "threads": "num:c_int",
        "cores": "num:c_int",
        "sockets": "num:c_int",
        "nnodes": "num:c_int",
        "totalcpus": "num:c_int",
        "vendor": "num:c_int",
        "vendor_string": "str:",
        "model": "num:c_int",
        "model_string": "str:",
        "revision": "num:c_float",
        "cpuid_family": "num:c_int",
        "cpuid_model": "num:c_int",
        "cpuid_stepping": "num:c_int",
        "cpu_max_mhz": "num:c_int",
        "cpu_min_mhz": "num:c_int",
        "virtualized": "num:c_int",
        "virtual_vendor_string": "str:",
        "virtual_vendor_version": "str:",
    }

    s_field = {"mem_hierarchy": (MH_info, 1)}


class ADDR_p(PAPI_Base):
    """Address pointer class."""

    def __init__(self, cdata):
        if cdata == ffi.NULL:
            self.addr = None
        else:
            self.addr = int(cdata.__repr__().split()[-1].strip()[:-1], base=16)

    def __repr__(self):
        return f"ADDR_p(addr={hex(self.addr) if self.addr is not None else 'NULL'})"


class ADDR_map(PAPI_Base):
    """Address map class. Maps to PAPI_address_map_t data structure."""

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
    """Executable info class. Maps to PAPI_exe_info_t data structure."""

    fields = {
        "fullname": "str:",
    }

    s_field = {"address_info": (ADDR_map, 0)}


class COMPONENT_info(PAPI_Base):
    """Component info class. Maps to PAPI_component_info_t data structure."""

    fields = {
        "name": "str:",
        "short_name": "str:",
        "description": "str:",
        "version": "str:",
        "support_version": "str:",
        "kernel_version": "str:",
        "disabled_reason": "str:",
        "disabled": "num:c_int",
        "CmpIdx": "num:c_int",
        "num_cntrs": "num:c_int",
        "num_mpx_cntrs": "num:c_int",
        "num_preset_events": "num:c_int",
        "num_native_events": "num:c_int",
        "default_domain": "num:c_int",
        "available_domains": "num:c_int",
        "default_granularity": "num:c_int",
        "available_granularities": "num:c_int",
        "hardware_intr_sig": "num:c_int",
        "component_type": "num:c_int",
        "pmu_names": "arr:str:",
        "reserved": "arr:num:c_uint",
        "hardware_intr": "num:c_uint",
        "precise_intr": "num:c_uint",
        "posix1b_timers": "num:c_uint",
        "kernel_profile": "num:c_uint",
        "kernel_multiplex": "num:c_uint",
        "fast_counter_read": "num:c_uint",
        "fast_real_timer": "num:c_uint",
        "fast_virtual_timer": "num:c_uint",
        "attach": "num:c_uint",
        "attach_must_ptrace": "num:c_uint",
        "cntr_umasks": "num:c_uint",
        "cpu": "num:c_uint",
        "inherit": "num:c_uint",
        "reserved_bits": "num:c_uint",
    }


class SHARED_LIB_info(PAPI_Base):
    """Shared Lib info class. Maps to PAPI_shlib_info_t data structure."""

    fields = {
        "count": "num:c_int",
    }

    s_fields = {"map": (ADDR_map, "count")}


Flips = namedtuple("Flips", "event rtime ptime flpins mflips")

Flops = namedtuple("Flops", "event rtime ptime flpops mflops")

IPC = namedtuple("IPC", "rtime ptime ins ipc")

EPC = namedtuple("EPC", "rtime ptime ref core evt epc")
