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

#pragma once
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define ARGS_FAULT 1
#define MEM_FAULT 2

#define PARG_SZ 6

#define PARG_IDX_D 0
#define PARG_IDX_H 1
#define PARG_IDX_M 2
#define PARG_IDX_S 3
#define PARG_IDX_V 4
#define PARG_IDX_FILE 5

const char PARG_OPT_D[] = "-d";
const char PARG_OPT_H[] = "-h";
const char PARG_OPT_M[] = "-m";
const char PARG_OPT_S[] = "-s";
const char PARG_OPT_V[] = "-v";

const char ARG_BANNER_MSG[] = "grasolbf [-h] [options] file \n\
BrainFuck Interpreter by Grasol \n\n\
version 0.1 \n\
";

const char ARG_HELP_MSG[] = " \n\
-d       : disable extended characters from interpreting \n\
-h       : display help \n\
-m size  : set memory size. Default is 65536 \n\
-s index : set start index of pointer of memory. Default is 0 \n\
-v       : allow overflow of pointer of memory \n\
";

bool parseArg(int argc, char **argv, int *parg);

#define DEFAULT_MEMORY_SZ 65536

struct File {
  char *data;
  size_t sz;
};
typedef struct File File;

bool fileOpen(char *name, File *file);