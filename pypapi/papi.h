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
#define PAPI_EATTR      -22    /**< Invalid or missing event attributes */
#define PAPI_ECOUNT     -23    /**< Too many events or attributes */
#define PAPI_ECOMBO     -24    /**< Bad combination of features */
#define PAPI_NUM_ERRORS  25    /**< Number of error messages specified in this API */


// PAPI HL from papi.h (definitions from papi.h)

int PAPI_accum_counters(long long * values, int array_len); /**< add current counts to array and reset counters */
int PAPI_num_counters(void); /**< get the number of hardware counters available on the system */
int PAPI_num_components(void); /**< get the number of components available on the system */
int PAPI_read_counters(long long * values, int array_len); /**< copy current counts to array and reset counters */
int PAPI_start_counters(int *events, int array_len); /**< start counting hardware events */
int PAPI_stop_counters(long long * values, int array_len); /**< stop counters and return current counts */
int PAPI_flips(float *rtime, float *ptime, long long * flpins, float *mflips); /**< simplified call to get Mflips/s (floating point instruction rate), real and processor time */
int PAPI_flops(float *rtime, float *ptime, long long * flpops, float *mflops); /**< simplified call to get Mflops/s (floating point operation rate), real and processor time */
int PAPI_ipc(float *rtime, float *ptime, long long * ins, float *ipc); /**< gets instructions per cycle, real and processor time */
int PAPI_epc(int event, float *rtime, float *ptime, long long *ref, long long *core, long long *evt, float *epc); /**< gets (named) events per cycle, real and processor time, reference and core cycles */
