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
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define ARGS_FAULT 1
#define MEM_FAULT 2

struct BF {
  uint8_t *memory;
  size_t mem_sz;
  size_t ptr1;
  size_t ptr2;

  char *idata;
  size_t isz;
  size_t iptr;

  bool ex_instr;
  bool ptr_overflow;
};
typedef struct BF BF;

#define BF_INC '+'
#define BF_DEC '-'
#define BF_PTR_INC '>'
#define BF_PTR_DEC '<'
#define BF_OUT '.'
#define BF_IN ','
#define BF_LOOP '['
#define BF_ENDLOOP ']'
#define BF_COPYT0 '/'
#define BF_COPYT1 '?'
#define BF_HALT '#'
#define BF_PTR_ZERO '$'
#define BF_PTR_XCHG '%'

#define BF_JUMP_EXCEPTION 1

BF *bfInit(size_t mem_sz);

int bfInterpreter(BF *bf);

void bfErrCodeDisplay(BF *bf, int err_code);