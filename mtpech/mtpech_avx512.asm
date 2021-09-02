[bits 64]
global mtpech_avx512

section .data
mask01 db 0x01
mask03 db 0x03
mask09 db 0x09
mask0a db 0x0a

section .text
mtpech_avx512:
    ; args + 8*0 - i, start
    ; args + 8*1 - end
    ; args + 8*3 - *numl
    ; ymm1 - bcd_num
  
    push rsi
    mov rsi, rcx
    xor rax, rax
    mov rcx, [rsi + 8*1]
    sub rcx, [rsi + 8*0]
    jb .end

    inc rcx
    mov r11, [rsi + 8*3]
    vmovdqu ymm1, [r11]
    vpbroadcastb ymm8, [mask01]
    vpbroadcastb ymm9, [mask03]
    vpbroadcastb ymm10, [mask09]
    vpbroadcastb ymm11, [mask0a]

    mov r10d, 0x55555555
    kmovd k3, r10d
    mov r11d, 1
    kmovd k4, r11d

.next: 
    vpcmpeqb k1, ymm1, ymm8
    vpcmpeqb k2, ymm1, ymm9
    kmovd r8d, k1
    shr r8d, 1
    kmovd r9d, k2 
    test r8d, r9d
    jz .false

    vmovdqu ymm2, ymm1
    vmovdqu8 ymm3 {k3}{z}, ymm1
    vpsrlw ymm2, ymm2, 8
    vpaddw ymm2, ymm2, ymm3
    vphaddw ymm2, ymm2, ymm2
    vphaddw ymm2, ymm2, ymm2
    vphaddw ymm2, ymm2, ymm2
    vperm2i128 ymm3, ymm2, ymm2, 1
    vpaddw xmm3, xmm3, xmm2
    pextrw r10, xmm3, 0
    cmp r10, 13
    jne .false

    inc rax

.false:
    dec rcx
    jz .end

    vpaddb ymm1 {k4}, ymm1, ymm8
    vpcmpb k1, ymm1, ymm10, 6
    kmovd r8d, k1
    test r8d, r8d
    jz .next

    vpcmpb k1, ymm1, ymm10, 1
    kmovd r8d, k1
    blsi r8d, r8d
    kmovd k1, r8d
    vpaddb ymm1 {k1}, ymm1, ymm8
    neg r8d
    kmovd k1, r8d
    vmovdqu8 ymm1 {k1}{z}, ymm1
    jmp .next

.end:
    mov [rsi + 8*2], rax
    pop rsi
    vzeroall
    ret
