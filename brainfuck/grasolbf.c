// Copyright 2022 Grasol
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "grasolbf.h"
#include "interpreter.h"

bool parseArg(int argc, char **argv, int *parg) {  
  if (argc < 2) {
    return false;
  }

  bool mem_sz = false;
  bool start_idx = false;  

  for (int i = 1; i < argc; i++) {
    char *arg = argv[i];

    if (mem_sz) {
      parg[PARG_IDX_M] = atoi(arg);
      mem_sz = false;
      continue;
    }

    if (start_idx) {
      parg[PARG_IDX_S] = atoi(arg);
      start_idx = false;
      continue;
    }

    if (!strcmp(arg, PARG_OPT_D)) {
      if (parg[PARG_IDX_D]) {
        return false;
      }

      parg[PARG_IDX_D] = 1;
    }

    else if (!strcmp(arg, PARG_OPT_H)) {
      if (parg[PARG_IDX_H]) {
        return false;
      }

      parg[PARG_IDX_H] = 1;
    }

    else if (!strcmp(arg, PARG_OPT_M)) {
      if (parg[PARG_IDX_M]) {
        return false;
      }

      mem_sz = true;
    }

    else if (!strcmp(arg, PARG_OPT_S)) {
      if (parg[PARG_IDX_S]) {
        return false;
      }

      start_idx = true;
    }

    else if (!strcmp(arg, PARG_OPT_V)) {
      if (parg[PARG_IDX_V]) {
        return false;
      }

      parg[PARG_IDX_V] = 1;
    }

    else {
      if (arg[0] == '-') {
        return false;
      }

      if (parg[PARG_IDX_FILE]) {
        return false;
      }

      parg[PARG_IDX_FILE] = i;
    }
  }

  if (mem_sz || start_idx) {
    return false;
  }

  if (parg[PARG_IDX_M] == 0) {
    parg[PARG_IDX_M] = DEFAULT_MEMORY_SZ;
  }

  return true;
}

bool fileOpen(char *name, File *file) {
  FILE *f = fopen(name, "r");
  if (f == NULL) {
    return false;
  }

  fseek(f, 0, SEEK_END);
  file->sz = ftell(f);
  fseek(f, 0, SEEK_SET);

  file->data = malloc(file->sz);
  if (file->data == NULL) {
    exit(MEM_FAULT);
  }

  fread(file->data, 1, file->sz, f);

  fclose(f);
  return true;
}


int main(int argc, char **argv) {
  // Argument parsing
  int parg[PARG_SZ] = {0};

  bool parse_ok = parseArg(argc, argv, parg);
  if (parg[PARG_IDX_H]) {
    fprintf(stderr, ARG_BANNER_MSG);
    fprintf(stderr, ARG_HELP_MSG);

    return 0;
  }

  if (!parse_ok || (parg[PARG_IDX_FILE] == 0)) {
    fprintf(stderr, ARG_BANNER_MSG);
    
    return ARGS_FAULT;
  }

  // File reading
  File *file = malloc(sizeof(File));
  if (file == NULL) {
    exit(MEM_FAULT);
  }

  char *file_name = argv[parg[PARG_IDX_FILE]];
  bool file_ok = fileOpen(file_name, file);
  if (!file_ok) {
    fprintf(stderr, "Cannot open file: '%s'\n", file_name);

    return ARGS_FAULT;
  }

  // Run BrainFuck
  BF *bf = bfInit(parg[PARG_IDX_M]);
  bf->ptr1 = parg[PARG_IDX_S];
  bf->idata = file->data;
  bf->isz = file->sz;
  bf->ex_instr = (bool)!parg[PARG_IDX_D];
  bf->ptr_overflow = (bool)parg[PARG_IDX_V];

  int bf_err_code = bfInterpreter(bf);

  bfErrCodeDisplay(bf, bf_err_code);


  free(file->data);
  free(file);
  free(bf->memory);
  free(bf);
  return 0;
}