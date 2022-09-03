# Brainfuck interpreter and macro brainfuck

Brainfuck intepreter have 5 new command:
 - **/** \- copy to cell 0
 - **?** \- copy to cell 1
 - **#** \- halt
 - **$** \- back data pointer to cell 0
 - **%** \- exchange data pointeres

Interpreter have additional data pointer. First pointer is a the main pointer and this pointer is use. Second Pointer is additional. '%' command is use to swap which pointer use.

## Macro brainfuck

macrobf.py is set of macros to easier write programs in brainfuck. These macros use above 5 additional commands. Second pointer is a the macro pointer. 

#### Macros list:
1. Arithmetic:
  - **ADD(dst, src1, src2)** \- add
  - **SUB(dst, src1, src2)** \- subtract
  - **INC(dst)** \- increment by 1
  - **DEC(dst)** \- decrement by 1
2. Logic and compares:
  - **EQU(dst, src1, src2)** \- equal
  - **NEQ(dst, src1, src2)** \- not equal
3. The main pointer manipulation:
  - **PADD(src)** \- increment the main pointer
  - **PSUB(src)** \- decrement the main pointer
  - **PMOV(src)** \- move the main pointer
  - **PXCHG(src)** \- exchange pointers
4. Flow control:
  - **LOOP(src, tag)** \- entry to loop
  - **ENDLOOP(src, tag)** \- end of loop
  - **IF(src, tag)** \- if src then...
  - **ELSE(tag)** \- else... 
  - **ENDIF(tag)** \- end of if (or if ... else)
  - **HALT()** \- halt
5. Data transfer:
  - **MOV(dst, src)** \- mov data
  - **OUT(src)** \- put character from consol
  - **IN(dst)** \- get character from consol

#### Macros use following types of arguments:
 - Absolute: **C(value)** \- absolute value of cell in memory
 - Relativ: **P()** \- cell, at the main pointer
 - Immediate: **value** \- integer value 

#### TODO:
1. Debugging mode in interpreter
2. Rest of macros e.g. swap cells, greater than, multiply etc.
