// PAPI error code (definitions from papi.h)

#define PAPI_OK          0     /**< No error */
#define PAPI_EINVAL     -1     /**< Invalid argument */
#define PAPI_ENOMEM     -2     /**< Insufficient memory */
#define PAPI_ESYS       -3     /**< A System/C library call failed */
#define PAPI_ECMP       -4     /**< Not supported by component */
#define PAPI_ESBSTR     -4     /**< Backwards compatibility */
#define PAPI_ECLOST     -5     /**< Access to the counters was lost or interrupted */
#define PAPI_EBUG       -6     /**< Internal error, please send mail to the developers */
#define PAPI_ENOEVNT    -7     /**< Event does not exist */
#define PAPI_ECNFLCT    -8     /**< Event exists, but cannot be counted due to counter resource limitations */
#define PAPI_ENOTRUN    -9     /**< EventSet is currently not running */
#define PAPI_EISRUN     -10    /**< EventSet is currently counting */
#define PAPI_ENOEVST    -11    /**< No such EventSet Available */
#define PAPI_ENOTPRESET -12    /**< Event in argument is not a valid preset */
#define PAPI_ENOCNTR    -13    /**< Hardware does not support performance counters */
#define PAPI_EMISC      -14    /**< Unknown error code */
#define PAPI_EPERM      -15    /**< Permission level does not permit operation */
#define PAPI_ENOINIT    -16    /**< PAPI hasn't been initialized yet */
#define PAPI_ENOCMP     -17    /**< Component Index isn't set */
#define PAPI_ENOSUPP    -18    /**< Not supported */
#define PAPI_ENOIMPL    -19    /**< Not implemented */
#define PAPI_EBUF       -20    /**< Buffer size exceeded */
#define PAPI_EINVAL_DOM -21    /**< EventSet domain is not supported for the operation */
#define PAPI_EATTR		-22    /**< Invalid or missing event attributes */
#define PAPI_ECOUNT		-23    /**< Too many events or attributes */
#define PAPI_ECOMBO		-24    /**< Bad combination of features */
#define PAPI_ECMP_DISABLED	-25    /**< Component containing event is disabled */
#define PAPI_NUM_ERRORS	 26    /**< Number of error messages specified in this API */


// PAPI initialization state (definitions from papi.h)

#define PAPI_NOT_INITED           0
#define PAPI_LOW_LEVEL_INITED     1      /* Low level has called library init */
#define PAPI_HIGH_LEVEL_INITED    2      /* High level has called library init */
#define PAPI_THREAD_LEVEL_INITED  4      /* Threads have been inited */


// PAPI states (definitions from papi.h)

#define PAPI_STOPPED      0x01  /**< EventSet stopped */
#define PAPI_RUNNING      0x02  /**< EventSet running */
#define PAPI_PAUSED       0x04  /**< EventSet temp. disabled by the library */
#define PAPI_NOT_INIT     0x08  /**< EventSet defined, but not initialized */
#define PAPI_OVERFLOWING  0x10  /**< EventSet has overflowing enabled */
#define PAPI_PROFILING    0x20  /**< EventSet has profiling enabled */
#define PAPI_MULTIPLEXING 0x40  /**< EventSet has multiplexing enabled */
#define PAPI_ATTACHED     0x80  /**< EventSet is attached to another thread/process */
#define PAPI_CPU_ATTACHED 0x100 /**< EventSet is attached to a specific cpu (not counting thread of execution) */


// Other PAPI constants (definitions from papi.h)

#define PAPI_NULL       -1      /**<A nonexistent hardware event used as a placeholder */

// Masks

#define PAPI_NATIVE_MASK     0x40000000
#define PAPI_PRESET_MASK     0x80000000

// Option definitions

#define PAPI_MIN_STR_LEN        64      /* For small strings, like names & stuff */
#define PAPI_MAX_STR_LEN       128      /* For average run-of-the-mill strings */
#define PAPI_2MAX_STR_LEN      256      /* For somewhat longer run-of-the-mill strings */
#define PAPI_HUGE_STR_LEN     1024      /* This should be defined in terms of a system parameter */

#define PAPI_PMU_MAX           40      /* maximum number of pmu's supported by one component */

#define PAPI_MAX_INFO_TERMS  12		   /* should match PAPI_EVENTS_IN_DERIVED_EVENT defined in papi_internal.h */

// Memory Hierarchy 

#define PAPI_MH_MAX_LEVELS    6		   /* # descriptors for each TLB or cache level */
#define PAPI_MAX_MEM_HIERARCHY_LEVELS 	  4


// Debug levels

#define PAPI_QUIET       0      /**< Option to turn off automatic reporting of return codes < 0 to stderr. */
#define PAPI_VERB_ECONT  1      /**< Option to automatically report any return codes < 0 to stderr and continue. */
#define PAPI_VERB_ESTOP  2      /**< Option to automatically report any return codes < 0 to stderr and exit. */

// Domain definitions

#define PAPI_DOM_USER    0x1    /**< User context counted */
// #define PAPI_DOM_MIN     PAPI_DOM_USER
#define PAPI_DOM_KERNEL	 0x2    /**< Kernel/OS context counted */
#define PAPI_DOM_OTHER	 0x4    /**< Exception/transient mode (like user TLB misses ) */
#define PAPI_DOM_SUPERVISOR 0x8 /**< Supervisor/hypervisor context counted */
// #define PAPI_DOM_ALL	 (PAPI_DOM_USER|PAPI_DOM_KERNEL|PAPI_DOM_OTHER|PAPI_DOM_SUPERVISOR) /**< All contexts counted */
/* #define PAPI_DOM_DEFAULT PAPI_DOM_USER NOW DEFINED BY COMPONENT */
// #define PAPI_DOM_MAX     PAPI_DOM_ALL
#define PAPI_DOM_HWSPEC  0x80000000     /**< Flag that indicates we are not reading CPU like stuff. The lower 31 bits can be decoded by the component into something meaningful. i.e. SGI HUB counters */
    
// Granularity definitions

#define PAPI_GRN_THR     0x1    /**< PAPI counters for each individual thread */
// #define PAPI_GRN_MIN     PAPI_GRN_THR
#define PAPI_GRN_PROC    0x2    /**< PAPI counters for each individual process */
#define PAPI_GRN_PROCG   0x4    /**< PAPI counters for each individual process group */
#define PAPI_GRN_SYS     0x8    /**< PAPI counters for the current CPU, are you bound? */
#define PAPI_GRN_SYS_CPU 0x10   /**< PAPI counters for all CPUs individually */
// #define PAPI_GRN_MAX     PAPI_GRN_SYS_CPU

// Locking Mechanisms defines

#define PAPI_USR1_LOCK          	0x0    /**< User controlled locks */
#define PAPI_USR2_LOCK          	0x1    /**< User controlled locks */
#define PAPI_NUM_LOCK           	0x2    /**< Used with setting up array */
// #define PAPI_LOCK_USR1          	PAPI_USR1_LOCK
// #define PAPI_LOCK_USR2          	PAPI_USR2_LOCK
// #define PAPI_LOCK_NUM			PAPI_NUM_LOCK


// FLIPS/FLOPS defines
#define PAPI_FP_INS  52	/*Floating point instructions executed */
#define PAPI_VEC_SP  105	/* Single precision vector/SIMD instructions */
#define PAPI_VEC_DP  106	/* Double precision vector/SIMD instructions */
#define PAPI_FP_OPS  102	/*Floating point operations executed */
#define PAPI_SP_OPS  103	/* Floating point operations executed; optimized to count scaled single precision vector operations */
#define PAPI_DP_OPS  104	/* Floating point operations executed; optimized to count scaled double precision vector operations */

// PAPI data structures

typedef char *__caddr_t;
typedef __caddr_t caddr_t;

typedef struct _papi_address_map {
    char name[PAPI_HUGE_STR_LEN];
    caddr_t text_start;       /**< Start address of program text segment */
    caddr_t text_end;         /**< End address of program text segment */
    caddr_t data_start;       /**< Start address of program data segment */
    caddr_t data_end;         /**< End address of program data segment */
    caddr_t bss_start;        /**< Start address of program bss segment */
    caddr_t bss_end;          /**< End address of program bss segment */
} PAPI_address_map_t;

typedef struct _papi_program_info {
    char fullname[PAPI_HUGE_STR_LEN];  /**< path + name */
    PAPI_address_map_t address_info;	 /**< executable's address space info */
} PAPI_exe_info_t;

typedef struct _dmem_t {
    long long peak;
    long long size;
    long long resident;
    long long high_water_mark;
    long long shared;
    long long text;
    long long library;
    long long heap;
    long long locked;
    long long stack;
    long long pagesize;
    long long pte;
} PAPI_dmem_info_t;

typedef struct event_info {
    unsigned int event_code;             /**< preset (0x8xxxxxxx) or 
                                            native (0x4xxxxxxx) event code */
    char symbol[PAPI_HUGE_STR_LEN];      /**< name of the event */
    char short_descr[PAPI_MIN_STR_LEN];  /**< a short description suitable for 
                                            use as a label */
    char long_descr[PAPI_HUGE_STR_LEN];  /**< a longer description:
                                            typically a sentence for presets,
                                            possibly a paragraph from vendor
                                            docs for native events */

    int component_index;           /**< component this event belongs to */
    char units[PAPI_MIN_STR_LEN];  /**< units event is measured in */
    int location;                  /**< location event applies to */
    int data_type;                 /**< data type returned by PAPI */
    int value_type;                /**< sum or absolute */
    int timescope;                 /**< from start, etc. */
    int update_type;               /**< how event is updated */
    int update_freq;               /**< how frequently event is updated */

    /* PRESET SPECIFIC FIELDS FOLLOW */



    unsigned int count;                /**< number of terms (usually 1) 
                                            in the code and name fields 
                                            - presets: these are native events
                                            - native: these are unused */

    unsigned int event_type;           /**< event type or category 
                                            for preset events only */

    char derived[PAPI_MIN_STR_LEN];    /**< name of the derived type
                                            - presets: usually NOT_DERIVED
                                            - native: empty string */
    char postfix[PAPI_2MAX_STR_LEN];   /**< string containing postfix 
                                            operations; only defined for 
                                            preset events of derived type 
                                            DERIVED_POSTFIX */

    unsigned int code[PAPI_MAX_INFO_TERMS]; /**< array of values that further 
                                            describe the event:
                                            - presets: native event_code values
                                            - native:, register values(?) */

    char name[PAPI_MAX_INFO_TERMS]         /**< names of code terms: */
            [PAPI_2MAX_STR_LEN];          /**< - presets: native event names,
                                                - native: descriptive strings 
                        for each register value(?) */

    char note[PAPI_HUGE_STR_LEN];          /**< an optional developer note 
                                            supplied with a preset event
                                            to delineate platform specific 
                    anomalies or restrictions */

} PAPI_event_info_t;

typedef struct _papi_mh_tlb_info {
    int type; /**< Empty, instr, data, vector, unified */
    int num_entries;
    int page_size;
    int associativity;
} PAPI_mh_tlb_info_t;

typedef struct _papi_mh_cache_info {
    int type; /**< Empty, instr, data, vector, trace, unified */
    int size;
    int line_size;
    int num_lines;
    int associativity;
} PAPI_mh_cache_info_t;

typedef struct _papi_mh_level_info {
    PAPI_mh_tlb_info_t   tlb[PAPI_MH_MAX_LEVELS];
    PAPI_mh_cache_info_t cache[PAPI_MH_MAX_LEVELS];
} PAPI_mh_level_t;

typedef struct _papi_mh_info { 
    int levels;
    PAPI_mh_level_t level[PAPI_MAX_MEM_HIERARCHY_LEVELS];
} PAPI_mh_info_t;

typedef struct _papi_hw_info {
    int ncpu;                     /**< Number of CPUs per NUMA Node */
    int threads;                  /**< Number of hdw threads per core */
    int cores;                    /**< Number of cores per socket */
    int sockets;                  /**< Number of sockets */
    int nnodes;                   /**< Total Number of NUMA Nodes */
    int totalcpus;                /**< Total number of CPUs in the entire system */
    int vendor;                   /**< Vendor number of CPU */
    char vendor_string[PAPI_MAX_STR_LEN];     /**< Vendor string of CPU */
    int model;                    /**< Model number of CPU */
    char model_string[PAPI_MAX_STR_LEN];      /**< Model string of CPU */
    float revision;               /**< Revision of CPU */
    int cpuid_family;             /**< cpuid family */
    int cpuid_model;              /**< cpuid model */
    int cpuid_stepping;           /**< cpuid stepping */

    int cpu_max_mhz;              /**< Maximum supported CPU speed */
    int cpu_min_mhz;              /**< Minimum supported CPU speed */

    PAPI_mh_info_t mem_hierarchy; /**< PAPI memory hierarchy description */
    int virtualized;              /**< Running in virtual machine */
    char virtual_vendor_string[PAPI_MAX_STR_LEN]; 
                                /**< Vendor for virtual machine */
    char virtual_vendor_version[PAPI_MAX_STR_LEN];
                                /**< Version of virtual machine */

    /* Legacy Values, do not use */
    float mhz;                    /**< Deprecated */
    int clock_mhz;                /**< Deprecated */

    /* For future expansion */
    int reserved[8];

} PAPI_hw_info_t;

typedef struct _papi_component_option {
    char name[PAPI_MAX_STR_LEN];            /**< Name of the component we're using */
    char short_name[PAPI_MIN_STR_LEN];      /**< Short name of component,
                    to be prepended to event names */
    char description[PAPI_MAX_STR_LEN];     /**< Description of the component */
    char version[PAPI_MIN_STR_LEN];         /**< Version of this component */
    char support_version[PAPI_MIN_STR_LEN]; /**< Version of the support library */
    char kernel_version[PAPI_MIN_STR_LEN];  /**< Version of the kernel PMC support driver */
    char disabled_reason[PAPI_MAX_STR_LEN]; /**< Reason for failure of initialization */
    int disabled;   /**< 0 if enabled, otherwise error code from initialization */
    int CmpIdx;				/**< Index into the vector array for this component; set at init time */
    int num_cntrs;               /**< Number of hardware counters the component supports */
    int num_mpx_cntrs;           /**< Number of hardware counters the component or PAPI can multiplex supports */
    int num_preset_events;       /**< Number of preset events the component supports */
    int num_native_events;       /**< Number of native events the component supports */
    int default_domain;          /**< The default domain when this component is used */
    int available_domains;       /**< Available domains */ 
    int default_granularity;     /**< The default granularity when this component is used */
    int available_granularities; /**< Available granularities */
    int hardware_intr_sig;       /**< Signal used by hardware to deliver PMC events */
//   int opcode_match_width;      /**< Width of opcode matcher if exists, 0 if not */
    int component_type;          /**< Type of component */
    char *pmu_names[PAPI_PMU_MAX];         /**< list of pmu names supported by this component */
    int reserved[8];             /* */
    unsigned int hardware_intr:1;         /**< hw overflow intr, does not need to be emulated in software*/
    unsigned int precise_intr:1;          /**< Performance interrupts happen precisely */
    unsigned int posix1b_timers:1;        /**< Using POSIX 1b interval timers (timer_create) instead of setitimer */
    unsigned int kernel_profile:1;        /**< Has kernel profiling support (buffered interrupts or sprofil-like) */
    unsigned int kernel_multiplex:1;      /**< In kernel multiplexing */
//   unsigned int data_address_range:1;    /**< Supports data address range limiting */
//   unsigned int instr_address_range:1;   /**< Supports instruction address range limiting */
    unsigned int fast_counter_read:1;     /**< Supports a user level PMC read instruction */
    unsigned int fast_real_timer:1;       /**< Supports a fast real timer */
    unsigned int fast_virtual_timer:1;    /**< Supports a fast virtual timer */
    unsigned int attach:1;                /**< Supports attach */
    unsigned int attach_must_ptrace:1;	   /**< Attach must first ptrace and stop the thread/process*/
//   unsigned int edge_detect:1;           /**< Supports edge detection on events */
//   unsigned int invert:1;                /**< Supports invert detection on events */
//   unsigned int profile_ear:1;      	   /**< Supports data/instr/tlb miss address sampling */
//     unsigned int cntr_groups:1;           /**< Underlying hardware uses counter groups (e.g. POWER5)*/
    unsigned int cntr_umasks:1;           /**< counters have unit masks */
//   unsigned int cntr_IEAR_events:1;      /**< counters support instr event addr register */
//   unsigned int cntr_DEAR_events:1;      /**< counters support data event addr register */
//   unsigned int cntr_OPCM_events:1;      /**< counter events support opcode matching */
    /* This should be a granularity option */
    unsigned int cpu:1;                   /**< Supports specifying cpu number to use with event set */
    unsigned int inherit:1;               /**< Supports child processes inheriting parents counters */
    unsigned int reserved_bits:12;
} PAPI_component_info_t;

typedef struct _papi_shared_lib_info {
    PAPI_address_map_t *map;
    int count;
} PAPI_shlib_info_t;

// PAPI HIGH (definitions from papi.h)

int PAPI_hl_region_begin(const char* region); /**< read performance events at the beginning of a region */
int PAPI_hl_read(const char* region); /**< read performance events inside of a region and store the difference to the corresponding beginning of the region */
int PAPI_hl_region_end(const char* region); /**< read performance events at the end of a region and store the difference to the corresponding beginning of the region */
int PAPI_hl_stop(); /**< stops a running high-level event set */

// PAPI LOW (definitions from papi.h)
// (commented definitions are not (yet?) binded)

int PAPI_accum(int EventSet, long long * values); /**< accumulate and reset hardware events from an event set */
int PAPI_add_event(int EventSet, int Event); /**< add single PAPI preset or native hardware event to an event set */
int PAPI_add_named_event(int EventSet, const char *EventName); /**< add an event by name to a PAPI event set */
int PAPI_add_events(int EventSet, int *Events, int number); /**< add array of PAPI preset or native hardware events to an event set */
int PAPI_assign_eventset_component(int EventSet, int cidx); /**< assign a component index to an existing but empty eventset */
int PAPI_attach(int EventSet, unsigned long tid); /**< attach specified event set to a specific process or thread id */
int PAPI_cleanup_eventset(int EventSet); /**< remove all PAPI events from an event set */
int PAPI_create_eventset(int *EventSet); /**< create a new empty PAPI event set */
int PAPI_detach(int EventSet); /**< detach specified event set from a previously specified process or thread id */
int PAPI_destroy_eventset(int *EventSet); /**< deallocates memory associated with an empty PAPI event set */
int PAPI_enum_event(int *EventCode, int modifier); /**< return the event code for the next available preset or natvie event */
int PAPI_enum_cmp_event(int *EventCode, int modifier, int cidx); /**< return the event code for the next available component event */
int PAPI_event_code_to_name(int EventCode, char *out); /**< translate an integer PAPI event code into an ASCII PAPI preset or native name */
int PAPI_event_name_to_code(const char *in, int *out); /**< translate an ASCII PAPI preset or native name into an integer PAPI event code */
int PAPI_get_dmem_info(PAPI_dmem_info_t *dest); /**< get dynamic memory usage information */
int PAPI_get_event_info(int EventCode, PAPI_event_info_t * info); /**< get the name and descriptions for a given preset or native event code */
const PAPI_exe_info_t *PAPI_get_executable_info(void); /**< get the executable's address space information */
const PAPI_hw_info_t *PAPI_get_hardware_info(void); /**< get information about the system hardware */
const PAPI_component_info_t *PAPI_get_component_info(int cidx); /**< get information about the component features */
int PAPI_get_multiplex(int EventSet); /**< get the multiplexing status of specified event set */
// int PAPI_get_opt(int option, PAPI_option_t * ptr); /**< query the option settings of the PAPI library or a specific event set */
// int PAPI_get_cmp_opt(int option, PAPI_option_t * ptr,int cidx); /**< query the component specific option settings of a specific event set */
long long PAPI_get_real_cyc(void); /**< return the total number of cycles since some arbitrary starting point */
long long PAPI_get_real_nsec(void); /**< return the total number of nanoseconds since some arbitrary starting point */
long long PAPI_get_real_usec(void); /**< return the total number of microseconds since some arbitrary starting point */
const PAPI_shlib_info_t *PAPI_get_shared_lib_info(void); /**< get information about the shared libraries used by the process */
// int PAPI_get_thr_specific(int tag, void **ptr); /**< return a pointer to a thread specific stored data structure */
// int PAPI_get_overflow_event_index(int Eventset, long long overflow_vector, int *array, int *number); /**< # decomposes an overflow_vector into an event index array */
long long PAPI_get_virt_cyc(void); /**< return the process cycles since some arbitrary starting point */
long long PAPI_get_virt_nsec(void); /**< return the process nanoseconds since some arbitrary starting point */
long long PAPI_get_virt_usec(void); /**< return the process microseconds since some arbitrary starting point */
int PAPI_is_initialized(void); /**< return the initialized state of the PAPI library */
int PAPI_library_init(int version); /**< initialize the PAPI library */
int PAPI_list_events(int EventSet, int *Events, int *number); /**< list the events that are members of an event set */
int PAPI_list_threads(unsigned long *tids, int *number); /**< list the thread ids currently known to PAPI */
int PAPI_lock(int); /**< lock one of two PAPI internal user mutex variables */
int PAPI_multiplex_init(void); /**< initialize multiplex support in the PAPI library */
int PAPI_num_cmp_hwctrs(int cidx); /**< return the number of hardware counters for a specified component */
int PAPI_num_events(int EventSet); /**< return the number of events in an event set */
// int PAPI_overflow(int EventSet, int EventCode, int threshold, int flags, PAPI_overflow_handler_t handler); /**< set up an event set to begin registering overflows */
void PAPI_perror(const char *msg ); /**< Print a PAPI error message */
// int PAPI_profil(void *buf, unsigned bufsiz, caddr_t offset, unsigned scale, int EventSet, int EventCode, int threshold, int flags); /**< generate PC histogram data where hardware counter overflow occurs */
int PAPI_query_event(int EventCode); /**< query if a PAPI event exists */
int PAPI_query_named_event(const char *EventName); /**< query if a named PAPI event exists */
int PAPI_read(int EventSet, long long * values); /**< read hardware events from an event set with no reset */
int PAPI_read_ts(int EventSet, long long * values, long long *cyc); /**< read from an eventset with a real-time cycle timestamp */
int PAPI_register_thread(void); /**< inform PAPI of the existence of a new thread */
int PAPI_remove_event(int EventSet, int EventCode); /**< remove a hardware event from a PAPI event set */
int PAPI_remove_named_event(int EventSet, const char *EventName); /**< remove a named event from a PAPI event set */
int PAPI_remove_events(int EventSet, int *Events, int number); /**< remove an array of hardware events from a PAPI event set */
int PAPI_reset(int EventSet); /**< reset the hardware event counts in an event set */
int PAPI_set_debug(int level); /**< set the current debug level for PAPI */
int PAPI_set_cmp_domain(int domain, int cidx); /**< set the component specific default execution domain for new event sets */
int PAPI_set_domain(int domain); /**< set the default execution domain for new event sets  */
int PAPI_set_cmp_granularity(int granularity, int cidx); /**< set the component specific default granularity for new event sets */
int PAPI_set_granularity(int granularity); /**<set the default granularity for new event sets */
int PAPI_set_multiplex(int EventSet); /**< convert a standard event set to a multiplexed event set */
// int PAPI_set_opt(int option, PAPI_option_t * ptr); /**< change the option settings of the PAPI library or a specific event set */
// int PAPI_set_thr_specific(int tag, void *ptr); /**< save a pointer as a thread specific stored data structure */
void PAPI_shutdown(void); /**< finish using PAPI and free all related resources */
// int PAPI_sprofil(PAPI_sprofil_t * prof, int profcnt, int EventSet, int EventCode, int threshold, int flags); /**< generate hardware counter profiles from multiple code regions */
int PAPI_start(int EventSet); /**< start counting hardware events in an event set */
int PAPI_state(int EventSet, int *status); /**< return the counting state of an event set */
int PAPI_stop(int EventSet, long long * values); /**< stop counting hardware events in an event set and return current events */
char *PAPI_strerror(int); /**< return a pointer to the error name corresponding to a specified error code */
unsigned long PAPI_thread_id(void); /**< get the thread identifier of the current thread */
// int PAPI_thread_init(unsigned long (*id_fn) (void)); /**< initialize thread support in the PAPI library */
int PAPI_unlock(int); /**< unlock one of two PAPI internal user mutex variables */
int PAPI_unregister_thread(void); /**< inform PAPI that a previously registered thread is disappearing */
int PAPI_write(int EventSet, long long * values); /**< write counter values into counters */
int PAPI_get_event_component(int EventCode);  /**< return which component an EventCode belongs to */
int PAPI_get_eventset_component(int EventSet);  /**< return which component an EventSet is assigned to */
int PAPI_get_component_index(const char *name); /**< Return component index for component with matching name */
int PAPI_disable_component(int cidx); /**< Disables a component before init */
int PAPI_disable_component_by_name(const char *name ); /**< Disable, before library init, a component by name. */
int PAPI_num_components(void); /**< get the number of components available on the system */

int PAPI_flips_rate(int event, float *rtime, float *ptime, long long *flpins, float *mflips); /**< simplified call to get Mflips/s (floating point instruction rate), real and processor time */
int PAPI_flops_rate(int event, float *rtime, float *ptime, long long * flpops, float *mflops); /**< simplified call to get Mflops/s (floating point operation rate), real and processor time */
int PAPI_ipc(float *rtime, float *ptime, long long * ins, float *ipc); /**< gets instructions per cycle, real and processor time */
int PAPI_epc(int event, float *rtime, float *ptime, long long *ref, long long *core, long long *evt, float *epc); /**< gets (named) events per cycle, real and processor time, reference and core cycles */
int PAPI_rate_stop(); /**< stops a running event set of a rate function */
