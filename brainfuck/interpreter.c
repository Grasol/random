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

#include "interpreter.h"

BF *bfInit(size_t mem_sz) {
  BF *bf = malloc(sizeof(BF));
  if (bf == NULL) {
    exit(MEM_FAULT);
  }

  bf->memory = malloc(mem_sz);
  if (bf->memory == NULL) {
    exit(MEM_FAULT);
  }

  memset(bf->memory, 0, mem_sz);

  bf->mem_sz = mem_sz;
  bf->ptr1 = 0;
  bf->ptr2 = 0;

  bf->idata = NULL;
  bf->isz = 0;
  bf->iptr = 0;

  bf->ex_instr = true;
  bf->ptr_overflow = false;
  //bf->stop = false;

  return bf;
}

int bfInterpreter(BF *bf) {
  while (bf->iptr < bf->isz) {
    switch (bf->idata[bf->iptr]) {
    case BF_INC: {
      uint8_t c = bf->memory[bf->ptr1];
      if (c == UCHAR_MAX) {
        c = 0;
      }

      else {
        c++;
      }

      bf->memory[bf->ptr1] = c;
      break;
    }

    case BF_DEC: {
      uint8_t c = bf->memory[bf->ptr1];
      if (c == 0) {
        c = UCHAR_MAX;
      }

      else {
        c--;
      }

      bf->memory[bf->ptr1] = c;
      break;
    }

    case BF_PTR_INC: {
      if (bf->ptr1 + 1 == bf->mem_sz) {
        if (bf->ptr_overflow) {
          bf->ptr1 = 0;
        }

        // else: saturation
      }

      else {
        bf->ptr1++;
      }

      break;
    }

    case BF_PTR_DEC: {
      if (bf->ptr1 == 0) {
        if (bf->ptr_overflow) {
          bf->ptr1 = bf->mem_sz - 1;
        }

        // else: saturation
      }

      else {
        bf->ptr1--;
      }

      break;
    }

    case BF_OUT: {
      putchar(bf->memory[bf->ptr1]);
      break;
    }

    case BF_IN: {
      uint8_t c;
      
      scanf(" %c", &c);
      bf->memory[bf->ptr1] = c;
      break;
    }

    case BF_LOOP: {
      if (bf->memory[bf->ptr1] == 0) {
        size_t tmp_iptr = bf->iptr;
        uint32_t match = 1;
        while (match) {
          tmp_iptr++;
          if (tmp_iptr >= bf->isz) {
            return BF_JUMP_EXCEPTION;
          }

          switch (bf->idata[tmp_iptr]) {
          case '[': match++; break;
          case ']': match--; break;
          }
        }

        bf->iptr = tmp_iptr;
      }

      break;
    }

    case BF_ENDLOOP: {
      if (bf->memory[bf->ptr1]) {
        size_t tmp_iptr = bf->iptr;
        uint32_t match = 1;       
        while (match) {
          if (tmp_iptr == 0) {
            return BF_JUMP_EXCEPTION;
          }

          tmp_iptr--;
          switch (bf->idata[tmp_iptr]) {
          case '[': match--; break;
          case ']': match++; break;
          }
        }

        bf->iptr = tmp_iptr;
      }

      break;
    }

    // extended instruction
    case BF_COPYT0: {
      if (!bf->ex_instr) break;

      bf->memory[0] = bf->memory[bf->ptr1];
      break;
    }

    case BF_COPYT1: {
      if (!bf->ex_instr) break;

      bf->memory[1] = bf->memory[bf->ptr1];
      break;
    }

    case BF_HALT: {
      return 0;
    }

    case BF_PTR_ZERO: {
      if (!bf->ex_instr) break;

      bf->ptr1 = 0;
      break;
    }

    case BF_PTR_XCHG: {
      if (!bf->ex_instr) break;

      size_t tmp_ptr = bf->ptr1;
      bf->ptr1 = bf->ptr2;
      bf->ptr2 = tmp_ptr;
      break;
    }
    }

    bf->iptr++;
  }

  return 0;
}

void bfErrCodeDisplay(BF *bf, int err_code) {
  switch (err_code) {
  case BF_JUMP_EXCEPTION: {
    fprintf(stderr, "\nError in char: %I64u: Jump Exception\n", bf->iptr + 1); break;
  }
  }

  return;
}

