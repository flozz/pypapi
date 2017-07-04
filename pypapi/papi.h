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
