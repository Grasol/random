#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

#define ARGC_ERROR 1
#define MEMORY_ERROR 2
#define ZERO_THREADS 3


struct mtpech_avx512_args {
  uint64_t start_value;
  uint64_t end_value;
  uint64_t ret_value;
  uint8_t *numl;
}; struct mtpech_avx512_args;

DWORD mtpech_avx512(void *args);

void u64tobcd_avx512(uint8_t *num, uint64_t val);

int main(int argc, char *argv[]) {
  clock_t t1 = clock();
  if (argc < 3) {
    return ARGC_ERROR;
  }

  uint32_t th = atoi(argv[1]);
  if (th == 0)
    return ZERO_THREADS;

  uint64_t max_value = atoll(argv[2]);
  if (max_value == 0) {
    return 0;
  }

  uint64_t k = max_value / (uint64_t)th;
  uint64_t tstart = 0;
  uint64_t tend = k + max_value % th + 1;

  struct mtpech_avx512_args *args[th];
  for (uint32_t i = 0; i < th; i++) {
    struct mtpech_avx512_args *arg = malloc(sizeof(struct mtpech_avx512_args));
    if (arg == NULL) 
      return MEMORY_ERROR;
    
    args[i] = arg;
    arg->start_value = tstart;
    arg->end_value = tend - 1;

    arg->numl = malloc(sizeof(uint8_t) * 64);
    if (arg->numl == NULL) 
      return MEMORY_ERROR;
    
    u64tobcd_avx512(args[i]->numl, tstart);


    tstart = tend;
    tend += k;
    if (tstart >= tend) {
      th = i + 1;
      break;
    }
  }

  HANDLE h[th];
  for (uint32_t i = 0; i < th; i++) {
    printf("Thread #%u: %llu-%llu\n", 
      i, args[i]->start_value, args[i]->end_value);
    h[i] = CreateThread(0, 0, mtpech_avx512, args[i], 0, 0);
  }

  WaitForMultipleObjects(th, h, TRUE, INFINITE);

  uint64_t sum = 0;
  for (uint32_t i = 0; i < th; i++) {
    sum += args[i]->ret_value;
  }

  clock_t t2 = clock();
  double t0 = (t2 - t1) / (double)CLOCKS_PER_SEC;
  printf("--> %llu \n%f sec \n", sum, t0);

  for (uint32_t i = 0; i < th; i++) {
    free(args[i]->numl);
    free(args[i]);
  }

  return 0;
}