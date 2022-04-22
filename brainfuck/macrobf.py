# Copyright 2022 Grasol
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import string

class MacroBFTypeError(TypeError):
  pass

class MacroBFValueError(ValueError):
  pass

class MacroBFTagError(Exception):
  pass


class Tags:
  def __init__(self):
    self.tags = ["$"]
    self.locals = [[]]
    self.ro_tags = ["$"]

  def _check(self, tag):
    if type(tag) is not str:
      raise MacroBFTypeError(f"tag '{tag}' must by string")

    if len(tag) == 1 and tag[0] in string.punctuation:
      raise MacroBFValueError(f"tag '{tag}' is not correct") 

    return

  def push(self, tag):
    self._check(tag)

    if tag[0] == ".": # local tag
      if tag in self.locals[-1]:
        raise MacroBFTagError(
          f"local tag '{self.tags[-1]}{tag}' has declareted yet")

      self.locals[-1].append(tag)

    else:
      if tag in self.ro_tags:
        raise MacroBFTagError(f"tag '{tag}' has declareted yet")

      self.tags.append(tag)
      self.locals.append([])
      self.ro_tags.append(tag)

    return

  def pop(self, tag):
    self.verify(tag)

    if tag[0] != ".":
      self.tags.pop()
      self.locals.pop()

    else:
      self.locals[-1].pop()

    return

  def verify(self, tag):
    self._check(tag)

    if tag[0] == ".": # local tag
      if len(self.locals) == 1 or tag != self.locals[-1][-1]:
        #print("AAAAAA", self.tags, self.locals)
        raise MacroBFTagError(
          f"local tag mismatch '{self.tags[-1]}{tag}'")

    else:
      if tag != self.tags[-1]:
        raise MacroBFTagError(f"tag mismatch '{tag}'")

    return

  def endCheck(self):
    if (self.tags[-1] != "$"):
      raise MacroBFTagError(f"tag '{self.tags[-1]} is not ending'")

tags = Tags()

class BF:
  def __init__(self):
    self.code = []
    self.macro_ptr = None

  def _genArrowMacroPtr(self, var):
    arrow = []
    if (self.macro_ptr is None):
      self.macro_ptr = 0
      arrow += ["$"]
  
    len = var - self.macro_ptr
    if (len > 0):
      arrow += [">"] * len
  
    elif (len < 0):
      alen = -len
      if (var + 1 < alen):
        arrow += ["$"]
        arrow += [">"] * var

      else:
        arrow += ["<"] * alen
  
    self.macro_ptr += len

    return arrow

  def save(self, file):
    tags.endCheck()

    data = ''.join(self.code)
    # epilogue optimalization
    # remove double %
    data = data.replace("%%", "")

    with open(file, "w") as f:
      f.write(data)

    return

    
bf = BF()

class C: # Cell
  def __init__(self, cell):
    self.cell = cell


class P: # Pointer
  def __init__(self, ptr=0):
    self.ptr = ptr
    self.arrow = []
    self.rarrow = []
    
    arrow = ["<"] * (-self.ptr)
    arrow2 = [">"] * self.ptr
    if self.ptr > 0:
      self.arrow, self.rarrow = arrow2, arrow

    else:
      self.arrow, self.rarrow = arrow, arrow2
      

def _checkArgs(args, pattern):
  for x in zip(args, pattern):
    x_type = type(x[0])
    if x_type not in x[1]:
      raise MacroBFTypeError(f"wrong type of argument '{x[0]}'") 

  return

def _loadArthArgs(src1, src2):
  code = []

  # first arg
  if type(src1) is P:
    code += src1.arrow
    code += ["/"]
    code += src1.rarrow

  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(src1.cell)
    code += ["/", "%"]

  # second arg
  if type(src2) is P:
    code += src2.arrow
    code += ["?"]
    code += src2.rarrow

  elif type(src2) is int:
    code += ["%", "$", ">", "[", "-", "]"]
    bf.macro_ptr = 1
    code += ["+"] * src2
    code += ["%"]
  
  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(src2.cell)
    code += ["?", "%"]

  return code

def _storeArthRes(dst):
  code = []

  if type(dst) is P:
    code += dst.arrow
    code += ["[", "-", "]", "%"]

    code += ["[", "-", "%", "+", "%", "]", "%"]
    code += dst.rarrow

  else:
    code += ["%", "$"]
    bf.macro_ptr = 0
    code += bf._genArrowMacroPtr(dst.cell)  
    code += ["[", "-", "]", "$"]
    bf.macro_ptr = 0

    code += ["[", "-"]
    code += bf._genArrowMacroPtr(dst.cell)
    code += ["+", "$"]
    code += ["]", "$", "%"]
    bf.macro_ptr = 0

  return code

#TODO: Pointers!

# ================================================================================
#                                 ARITHMETIC                                      
# --------------------------------------------------------------------------------
def ADD(dst, src1, src2):
  _checkArgs([dst, src1, src2], [[P, C], [P, C], [P, C, int]])
  code = []

  code += _loadArthArgs(src1, src2)

  # addition (result in cell 0)
  code += ["%", "$", ">"]
  bf.macro_ptr = 1
  code += ["[", "-", "<", "+", ">", "]", "%"]
  
  code += _storeArthRes(dst)

  bf.code += code
  return

# --------------------------------------------------------------------------------
def SUB(dst, src1, src2):
  _checkArgs([dst, src1, src2], [[P, C], [P, C], [P, C, int]])
  code = []

  code += _loadArthArgs(src1, src2)

  # subtraction (result in cell 0)
  code += ["%", "$", ">"]
  code += ["[", "-", "<", "-", ">", "]", "<", "%"]
  bf.macro_ptr = 0
  
  code += _storeArthRes(dst)

  bf.code += code
  return

# --------------------------------------------------------------------------------
def MUL(dsth, dstl, src1, src2):
  pass

# --------------------------------------------------------------------------------
def DIV(dstq, dstr, src1, src2):
  pass

# --------------------------------------------------------------------------------
def IMUL(dsth, dstl, src1, src2):
  pass

# --------------------------------------------------------------------------------
def IDIV(dstq, dstr, src1, src2):
  pass

# --------------------------------------------------------------------------------
def NEG(dst, src):
  pass

# --------------------------------------------------------------------------------
def INC(dst):
  _checkArgs([dst], [[P, C]])
  code = []

  if type(dst) is P:
    code += dst.arrow
    code += ["+"]
    code += dst.rarrow

  else:
    code = ["%"]
    code += bf._genArrowMacroPtr(dst.cell)
    code += ["+", "%"]
  
  bf.code += code
  return

# --------------------------------------------------------------------------------
def DEC(dst):
  _checkArgs([dst], [[P, C]])
  code = []

  if type(dst) is P:
    code += dst.arrow
    code += ["-"]
    code += dst.rarrow

  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(dst.cell)
    code += ["-", "%"]
  
  bf.code += code
  return

# ================================================================================
#                                   LOGIC                                         
# --------------------------------------------------------------------------------
def AND(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def OR(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def XOR(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def NOT(dst, src):
  pass

# --------------------------------------------------------------------------------
def EQU(dst, src1, src2):
  _checkArgs([dst, src1, src2], [[P, C], [P, C], [P, C, int]])
  code = []

  code += _loadArthArgs(src1, src2)

  # subtraction (result in cell 0)
  code += ["%", "$", ">"]
  bf.macro_ptr = 1
  code += ["[", "-", "<", "-", ">", "]"]

  # equal (result in cell 0)
  code += ["<", "[", "[", "-", "]", "-", ">", "]"]
  code += ["$", "+", "%"]
  macro_ptr = 0

  code += _storeArthRes(dst)

  bf.code += code
  return

# --------------------------------------------------------------------------------
def NEQ(dst, src1, src2):
  _checkArgs([dst, src1, src2], [[P, C], [P, C], [P, C, int]])
  code = []

  code += _loadArthArgs(src1, src2)

  # subtraction (result in cell 0)
  code += ["%", "$", ">"]
  bf.macro_ptr = 1
  code += ["[", "-", "<", "-", ">", "]"]

  # not equal (result in cell 0)
  code += ["<", "[", "[", "-", "]", "+", ">", "]"]
  code += ["$", "%"]
  macro_ptr = 0
  
  code += _storeArthRes(dst)

  bf.code += code
  return

# --------------------------------------------------------------------------------
def GRT(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def LSS(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def GEQ(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def LEQ(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def IGRT(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def ILSS(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def IGEQ(dst, src1, src2):
  pass

# --------------------------------------------------------------------------------
def ILEQ(dst, src1, src2):
  pass

# ================================================================================
#                               MEMORY POINTERS                                   
# --------------------------------------------------------------------------------
def PADD(src):
  _checkArgs([src], [[C, int]])
  code = []

  if type(src) is int:
    code += [">"] * src
  
  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(src.cell)
    code += ["/", "$"]
    bf.macro_ptr = 0

    code += ["[", "-", "%", ">", "%", "]"]
    code += ["%"]

  bf.code += code
  return 

# --------------------------------------------------------------------------------
def PSUB(src):
  _checkArgs([src], [[C, int]])
  code = []

  if type(src) is int:
    code += ["<"] * src
  
  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(src.cell)
    code += ["/", "$"]
    bf.macro_ptr = 0
    code += ["[", "-", "%", "<", "%", "]"]
    code += ["%"]

  bf.code += code
  return 

# --------------------------------------------------------------------------------
def PMOV(src):
  _checkArgs([src], [[C, int]])
  code = ["$"]

  if type(src) is int:
    code += [">"] * src
    
  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(src.cell)
    code += ["/", "$"]
    bf.macro_ptr = 0
    code += ["[", "-", "%", ">", "%", "]"]
    code += ["%"]

  bf.code += code
  return 

# --------------------------------------------------------------------------------
def PXCHG():
  bf.macro_ptr = None
  bf.code += ["%"]
  return

# ================================================================================
#                                FLOW CONTROL                                     
# --------------------------------------------------------------------------------
def LOOP(src, label=None):
  _checkArgs([src, label], [[P, C], [str, None]])
  # label checking
  if label is not None:
    tags.push(label)

  code = []

  if type(src) is P:
    code += src.arrow
    code += ["["]
    code += src.rarrow

  else:
    code += ["%", "$"]
    bf.macro_ptr = 0
    code += bf._genArrowMacroPtr(src.cell)
    code += ["[", "%"] # go to loop...

  bf.code += code
  return

# --------------------------------------------------------------------------------
def ENDLOOP(src, label=None):
  _checkArgs([src, label], [[P, C], [str, None]])
  # label checking
  if label is not None:
    tags.pop(label)

  code = []

  if type(src) is P:
    code += src.arrow
    code += ["]"]
    code += src.rarrow

  else:
    code += ["%", "$"]
    bf.macro_ptr = 0
    code += bf._genArrowMacroPtr(src.cell)
    code += ["]", "%"] 
  
  bf.code += code
  return

# --------------------------------------------------------------------------------
def IF(src, label=None):
  _checkArgs([src, label], [[C, P], [str, None]])
  # label checking
  if label is not None:
    tags.push(label)

  code = []

  code += ["%", "$", "[", "-", "]", "+"]
  bf.macro_ptr = 0
  code += bf._genArrowMacroPtr(src.cell)
  code += ["[", "%"] # go to if...

  bf.code += code
  return 

# --------------------------------------------------------------------------------
def ELSE(label=None):
  _checkArgs([label], [[str, None]])
  # label checking
  if label is not None:
    tags.verify(label)

  code = []

  code += ["%", "$", "[", "-", "]", "]"] # end if
  code += ["$", "[", "%"] # go to else...
  bf.macro_ptr = 0

  bf.code += code
  return 

# --------------------------------------------------------------------------------
def ENDIF(label=None):
  _checkArgs([label], [[str, None]])
  # label checking
  if label is not None:
    tags.pop(label)

  code = []

  code += ["%", "$", "[", "-", "]", "]", "$", "%"] # end if
  bf.macro_ptr = 0

  bf.code += code
  return 

# --------------------------------------------------------------------------------
def HALT():
  bf.code += ["#"]
  return

# ================================================================================
#                                 MOVING DATA                                     
# --------------------------------------------------------------------------------
def MOV(dst, src):
  _checkArgs([dst, src], [[P, C], [P, C, int]])
  code = []
  end = False

  if type(src) is P:
    code += src.arrow
    if (type(dst) is C) and (dst.cell == 1):
      code += ["?"]
      end = True

    else:
      code += ["/"]
      if (type(dst) is C) and (dst.cell == 0):
        end = True

    code += src.rarrow

  elif type(src) is C:
    code += ["%"]
    code += bf._genArrowMacroPtr(src.cell)
    if (type(dst) is C) and (dst.cell == 1):
      code += ["?"]
      end = True

    else:
      code += ["/"]
      if (type(dst) is C) and (dst.cell == 0):
        end = True

    code += ["%"]

  if not end:
    if type(dst) is P:
      code += dst.arrow
      code += ["[", "-", "]"]
      if type(src) is int:
        code += ["+"] * src

      else:
        code += ["%", "$", "[", "-", "%", "+", "%", "]", "%"]
        bf.macro_ptr = 0

      code += dst.rarrow

    elif type(dst) is C:
      code += ["%"]
      code += bf._genArrowMacroPtr(dst.cell)
      code += ["[", "-", "]"]
      if type(src) is int:
        code += ["+"] * src

      else:
        code += ["$", "[", "-"]
        bf.macro_ptr = 0
        code += bf._genArrowMacroPtr(dst.cell)
        code += ["+", "$", "]"]
        bf.macro_ptr = 0
        
      code += ["%"]

  bf.code += code
  return

# --------------------------------------------------------------------------------
def SWAP(dst1, dst2): # swap using cell0 and cell1 is undefined behavior
  pass



# --------------------------------------------------------------------------------
def OUT(src):
  _checkArgs([src], [[C, P, int]])
  code = []

  if type(src) is P:
    code += src.arrow
    code += ["."]
    code += src.rarrow

  elif type(src) is C:
    code += ["%"]
    code += bf._genArrowMacroPtr(src.cell)
    code += ["."]
    code += ["%"]

  else:
    code += ["%", "$", "[", "-", "]"]
    bf.macro_ptr = 0
    code += ["+"] * src
    code += [".", "%"]

  bf.code += code
  return

# --------------------------------------------------------------------------------
def IN(dst):
  _checkArgs([dst], [[C, P]])
  code = []

  if type(dst) is P:
    code += dst.arrow
    code += [","]
    code += dst.rarrow
    
  else:
    code += ["%"]
    code += bf._genArrowMacroPtr(dst.cell)
    code += [","]
    code += ["%"]

  bf.code += code
  return





