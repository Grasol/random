[bits 64]
global mtpech_avx512

section .data
mask01 db 0x01
mask03 db 0x03
mask0a db 0x0a


section .text
mtpech_avx512:
    ; rcx - max value
    ; r8 - i
    ; r9 - numl
    ; ymm1 - bcd_num
  
    push rsi
    mov rsi, rcx

    mov rcx, [rsi + 8*0]
    mov r8, [rsi + 8*1]
    mov r9, [rsi + 8*3]

    xor rax, rax
    test r8, r8 
    jz .end

    vmovdqu ymm1, [r9]
    vpbroadcastb ymm8, [mask01]
    vpbroadcastb ymm9, [mask03]
    vpbroadcastb ymm10, [mask0a]

    mov r11d, 0x55555555
    kmovd k6, r11d
.start: 
    vpcmpb k1, ymm1, ymm8, 0
    vpcmpb k2, ymm1, ymm9, 0 
    kshiftrd k1, k1, 1
    ktestd k1, k2
    jz .false

    vmovdqu ymm2, ymm1
    vmovdqu8 ymm3 {k6}{z}, ymm1
    vpsrlw ymm2, ymm2, 8
    vpaddw ymm2, ymm2, ymm3
    vphaddw ymm2, ymm2, ymm2
    vphaddw ymm2, ymm2, ymm2
    vphaddw ymm2, ymm2, ymm2
    vperm2i128 ymm3, ymm2, ymm2, 1
    vpaddw xmm3, xmm3, xmm2
    pextrw r11, xmm3, 0
    cmp r11, 13
    jne .false

    inc rax

.false:
    inc rcx
    cmp rcx, r8
    ja .end

    mov r11d, 1
    kmovd k4, r11d
.inc_loop:
    vpaddb ymm1 {k4}, ymm1, ymm8
    vpcmpb k4, ymm1, ymm10, 0
    ktestd k4, k4
    jz .start
    knotd k5, k4
    kshiftld k4, k4, 1
    vmovdqu8 ymm1 {k5}{z}, ymm1
    jmp .inc_loop

.end:
    mov [rsi + 8*2], rax
    pop rsi
    vzeroall
    ret
