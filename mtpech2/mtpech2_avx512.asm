[bits 64]
global mtpech_avx512

section .data
mask00 db 0x00
mask01 db 0x01
mask02 db 0x02
mask03 db 0x03
;mask09 db 0x09
mask0a db 0x0a
mask0d db 0x0d


section .text
mtpech_avx512:
    ; args + 8*0 - i, start
    ; args + 8*1 - end
    ; args + 8*3 - *numl
    ; ymm1 - bcd_num
    ;int3
    push rdx
    push rbx
    push rsi
    push r12
    push r13
    push r14
    mov rsi, rcx
    xor rax, rax
    mov rcx, [rsi + 8*1]
    sub rcx, [rsi + 8*0]
    jb .end

    add rcx, 2
    xor rdx, rdx
    mov r11, [rsi + 8*3]
    vmovdqu8 zmm1, [r11]
    vpbroadcastb zmm8, [mask01]
    vpbroadcastb zmm11, [mask02]
    vpbroadcastb zmm9, [mask03]
    vpbroadcastb zmm13, [mask0d]
    vpbroadcastb zmm10, [mask0a]

    mov r12, 0xffffffff00000000
    kmovq k1, r12
    vmovdqu8 zmm12 {k1}{z}, zmm8

    mov r13, 0xffffffff
    kmovq k5, r13

    mov r14, 0x0000000100000001
    kmovq k7, r14

    mov r10, 0x5555555555555555
    kmovq k6, r10

    mov rbx, 0xffffffff7fffffff

.next: 
    vpcmpb k1, zmm1, zmm8, 0
    vpcmpb k2, zmm1, zmm9, 0
    kmovq r8, k1
    shr r8, 1
    and r8, rbx
    kmovq r9, k2 
    and r8, r9
    jz .false

    vmovdqu8 zmm2, zmm1
    vmovdqu8 zmm3 {k6}{z}, zmm1
    vpsrlw zmm2, zmm2, 8
    vpaddw zmm2, zmm2, zmm3
    vshufi32x4 zmm3, zmm2, zmm2, 0b1110
    vphaddw ymm2, ymm2, ymm3
    vphaddw ymm2, ymm2, ymm2
    vphaddw ymm2, ymm2, ymm2
    vperm2i128 ymm3, ymm2, ymm2, 1
    vpaddw xmm3, xmm3, xmm2
    pextrw r10, xmm3, 0
    pextrw r11, xmm3, 1

    cmp r10, 13
    jne .cmp2
    test r8, r13
    jz .cmp2
    inc rax

.cmp2:
    cmp r11, 13
    jne .false
    test r8, r12
    jz .false
    inc rax

.false:
    sub rcx, 2
    jbe .end
    cmp rcx, 2
    jne .skip_hzero
    vmovdqu8 zmm1 {k5}{z}, zmm1

.skip_hzero:
;    int3
;    vpcmpb k4, zmm10, zmm1, 4 ; zmm1 != 9
;    kmovq r8, k4
;    mov r9, r8
;    and r8, r13 ; first mask
;    shr r9, 32  ; second mask
;
;    blsi r8, r8
;    blsi r9, r9
;    mov r10, r9
;    shl r9, 32
;    or r9, r8
;    kmovq k4, r9
;    vpaddb zmm1 {k4}, zmm1, zmm11
;
;    dec r8
;    dec r10
;    shl r10, 32
;    or r8, r10
;    not r8
;    kmovq k4, r8
;    vmovdqu8 zmm1 {k4}{z}, zmm1
;    jmp .next
;

    vpaddb zmm1 {k7}, zmm1, zmm11
.inc_loop:    
    vpcmpb k4, zmm10, zmm1, 2
    kmovq r8, k4
    test r8, r8
    jz .next

    mov r11, 1
    shlx r8, r8, r11
    vpsubb zmm1 {k4}, zmm1, zmm10
    kmovq k4, r8
    vpaddb zmm1 {k4}, zmm1, zmm8
    jmp .inc_loop

.end:
    mov [rsi + 8*2], rax
    pop r14
    pop r13
    pop r12
    pop rsi
    pop rbx
    pop rdx
    vzeroall
    ret
