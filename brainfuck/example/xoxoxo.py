from macrobf import *

GAME = 0x20
TURN = 0x21 # 1:O 2:X
INPUT_CH = 0x22
CH_SPACE = 0x24
CH_O = 0x25
CH_X = 0x26

TILE_IDX = 0x23
TILE_BOARD = 0x31 # 0:empty 1:O 2:X

WIN_PATTERN_IDX = 0x28
WIN_PLAYER = 0x29
WIN_RET = 0x2a
END_WIN = 0x2f
WIN_PATTERN_COUNTER = 0x2b
WIN_PATTERN_PTR = 0x40
WIN_PATTERNS = (
  "\1\1\1\0\0\0\0\0\0"
  "\0\0\0\1\1\1\0\0\0"
  "\0\0\0\0\0\0\1\1\1"
  "\1\0\0\1\0\0\1\0\0"
  "\0\1\0\0\1\0\0\1\0"
  "\0\0\1\0\0\1\0\0\1"
  "\1\0\0\0\1\0\0\0\1"
  "\0\0\1\0\1\0\1\0\0"
)

TURN_MSG_PTR = 0x90 # 0x90 - 0x97
TURN_MSG = "Turn: \1\n\0"

BOARD_MSG_IDX = 0x2c
BOARD_MSG_PTR = 0xa0 # 0xa0 - 0xda
BOARD_MSG = \
  " \1\7 | \1\10 | \1\11\n---+---+---\n \1\4 | \1\5 | \1\6\n---+---+---\n \1\1 | \1\2 | \1\3\n\0"

PLAYER_O_WIN_PTR = 0xf0
PLAYER_O_WIN_MSG = "Player o win!\n\0"
PLAYER_X_WIN_PTR = 0x100
PLAYER_X_WIN_MSG = "Player x win!\n\0"
DRAW_PTR = 0x110
DRAW_MSG = "Draw\n\0"

def checkWin():
  MOV(C(WIN_RET), 0)
  MOV(C(WIN_PATTERN_COUNTER), 8)
  MOV(C(WIN_PATTERN_IDX), WIN_PATTERN_PTR)

  MOV(C(0x18), 0)
  MOV(C(0x19), 0)
  MOV(C(0x1a), 0)
  MOV(C(0x1b), 0)
  MOV(C(0x1c), 0)
  MOV(C(0x1d), 0)
  MOV(C(0x1e), 0)
  MOV(C(0x1f), 0)

  LOOP(C(WIN_PATTERN_COUNTER), ".patter_loop")
  MOV(C(TILE_IDX), 0)
  MOV(C(0x10), 1)

  LOOP(C(0x10), ".tile_loop")
  PMOV(C(WIN_PATTERN_IDX))
  MOV(C(0x14), P())

  IF(C(0x14), ".pattern_one")
  ADD(C(0x12), C(TILE_IDX), TILE_BOARD)
  PMOV(C(0x12))
  EQU(C(0x12), P(), C(WIN_PLAYER))

  IF(C(0x12), ".inc_vars")
  MOV(C(0x13), 0x20)
  SUB(C(0x13), C(0x13), C(WIN_PATTERN_COUNTER))
  PMOV(C(0x13))
  INC(P())

  ENDIF(".inc_vars") 

  ENDIF(".pattern_one")
  INC(C(WIN_PATTERN_IDX))
  INC(C(TILE_IDX))
  NEQ(C(0x10), C(TILE_IDX), 9)

  ENDLOOP(C(0x10), ".tile_loop")
  DEC(C(WIN_PATTERN_COUNTER))

  ENDLOOP(C(WIN_PATTERN_COUNTER), ".patter_loop")


  PMOV(0x18)
  MOV(C(0x16), 8)
  
  LOOP(C(0x16), ".end_checker")
  EQU(C(0x10), P(), 3)

  IF(C(0x10), ".win")
  MOV(C(WIN_RET), 1)
  MOV(C(0x16), 1)

  ENDIF(".win")
  PADD(1)
  DEC(C(0x16))

  ENDLOOP(C(0x16), ".end_checker")

  return

def printTURNMsg():
  PMOV(TURN_MSG_PTR)

  LOOP(P(), ".print_TURN")
  EQU(C(0x10), P(), 1)

  IF(C(0x10), ".TURN_ch")
  EQU(C(0x11), C(TURN), 1)

  IF(C(0x11), ".TURN_ox")
  OUT(C(CH_O))

  ELSE(".TURN_ox")
  OUT(C(CH_X))

  ENDIF(".TURN_ox")

  ELSE(".TURN_ch")
  OUT(P())

  ENDIF(".TURN_ch")

  PADD(1)

  ENDLOOP(P(), ".print_TURN")

  return

def printBoard():
  MOV(C(TILE_IDX), 0)
  MOV(C(BOARD_MSG_IDX), 0)
  PMOV(BOARD_MSG_PTR)
  
  LOOP(P(), ".print_board")
  EQU(C(0x10), P(), 1)

  IF(C(0x10), ".tile_ch")
  PADD(1)
  INC(C(BOARD_MSG_IDX))

  ADD(C(0x11), P(), TILE_BOARD)
  DEC(C(0x11))
  PMOV(C(0x11))
  EQU(C(0x12), P(), 1)

  IF(C(0x12), ".tile_o")
  OUT(C(CH_O))

  ELSE(".tile_o")
  EQU(C(0x12), P(), 2)

  IF(C(0x12), ".tile_x")
  OUT(C(CH_X))

  ELSE(".tile_x")
  OUT(C(CH_SPACE))

  ENDIF(".tile_x")
  ENDIF(".tile_o")

  ELSE(".tile_ch")
  OUT(P())

  ENDIF(".tile_ch")

  INC(C(BOARD_MSG_IDX))
  PMOV(BOARD_MSG_PTR)
  PADD(C(BOARD_MSG_IDX))

  ENDLOOP(P(), ".print_board")

  return

def putString(mem_ptr, string):
  for i, s in enumerate(string):
    MOV(C(mem_ptr + i), ord(s))

  return 

def main():
  # init
  MOV(C(CH_SPACE), ord(" "))
  MOV(C(CH_O), ord("o"))
  MOV(C(CH_X), ord("x"))

  putString(WIN_PATTERN_PTR, WIN_PATTERNS)

  putString(TURN_MSG_PTR, TURN_MSG)

  putString(BOARD_MSG_PTR, BOARD_MSG)

  putString(PLAYER_O_WIN_PTR, PLAYER_O_WIN_MSG)

  putString(PLAYER_X_WIN_PTR, PLAYER_X_WIN_MSG)

  putString(DRAW_PTR, DRAW_MSG)

  MOV(C(GAME), 1)
  MOV(C(TURN), 1)
  MOV(C(INPUT_CH), 0)

  LOOP(C(GAME), "game_loop")
  
  printBoard()

  printTURNMsg()

  # input
  MOV(C(0x10), 1)

  LOOP(C(0x10), "in_loop")
  IN(C(INPUT_CH))

  # TODO: check valid INPUT_CH. 0x30 < INPUT_CH < 0x3a

  PMOV(C(INPUT_CH))
  EQU(C(0x10), P(), 0)

  IF(C(0x10), ".set_board")
  MOV(P(), C(TURN))
  MOV(C(INPUT_CH), 0)

  ELSE(".set_board")
  MOV(C(INPUT_CH), 1)

  ENDIF(".set_board")

  ENDLOOP(C(INPUT_CH), "in_loop")

  # check win
  MOV(C(WIN_PLAYER), 1)
  checkWin()

  IF(C(WIN_RET), "check_o_win")
  MOV(C(GAME), 0)
  MOV(C(END_WIN), 1)

  ELSE("check_o_win")
  MOV(C(WIN_PLAYER), 2)
  checkWin()

  IF(C(WIN_RET), "check_x_win")
  MOV(C(GAME), 0)
  MOV(C(END_WIN), 2)

  ENDIF("check_x_win")
  ENDIF("check_o_win")

  IF(C(GAME), "game_continue")
  # switch TURN
  EQU(C(0x10), C(TURN), 1)

  IF(C(0x10), "switch_TURN")
  MOV(C(TURN), 2)

  ELSE("switch_TURN")
  MOV(C(TURN), 1)

  ENDIF("switch_TURN")

  # check empty tiles to continue
  PMOV(TILE_BOARD)
  MOV(C(TILE_IDX), 9)
  MOV(C(0x11), 0)

  LOOP(C(TILE_IDX), "empty_tiles_check")
  EQU(C(0x10), P(), 0)

  IF(C(0x10), ".inc")
  INC(C(0x11))

  ENDIF(".inc")
  PADD(1)
  DEC(C(TILE_IDX))

  ENDLOOP(C(TILE_IDX), "empty_tiles_check")
  EQU(C(0x11), C(0x11), 0)

  IF(C(0x11), "draw")
  MOV(C(GAME), 0)
  MOV(C(END_WIN), 0)

  ENDIF("draw")
  ENDIF("game_continue")

  ENDLOOP(C(GAME) ,"game_loop")



  tags.push("end")

  printBoard()

  EQU(C(0x10), C(END_WIN), 0)

  IF(C(0x10), "end_win0")
  #print draw
  PMOV(DRAW_PTR)

  ELSE("end_win0")
  EQU(C(0x10), C(END_WIN), 1)

  IF(C(0x10), "end_win1")
  # print player o win
  PMOV(PLAYER_O_WIN_PTR)

  ELSE("end_win1")
  # print player x win
  PMOV(PLAYER_X_WIN_PTR)

  ENDIF("end_win1")
  ENDIF("end_win0")

  LOOP(P(), "end_print")
  OUT(P())
  PADD(1)

  ENDLOOP(P(), "end_print")

  tags.pop("end")

  return


if __name__ == "__main__":
  main()
  bf.save("xoxoxo.bf")