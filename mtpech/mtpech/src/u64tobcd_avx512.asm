[bits 64]
global u64tobcd_avx512

section .data
zero   db 0x00
mask01 db 0x01
mask03 db 0x03
mask05 db 0x05
mask0f db 0x0f
mask10 db 0x10

section .text
u64tobcd_avx512:
    ; rcx - *num output
    ; rdx - val input

    xor rax, rax
    mov r8, 64
    vpbroadcastb ymm0, [zero]
    vpbroadcastb ymm1, [mask01]
    vpbroadcastb ymm2, [mask03]
    vpbroadcastb ymm3, [mask05]
    vpbroadcastb ymm4, [mask0f]
    vpbroadcastb ymm5, [mask10]

.start:
    vpcmpb k1, ymm0, ymm3, 5
    vpaddb ymm0 {k1}, ymm0, ymm2
    vpsllw ymm0, ymm0, 1
    
    vpcmpb k1, ymm0, ymm5, 5
    kshiftld k1, k1, 1
    shl rdx, 1
    setc al
    kmovd k2, eax
    kord k1, k1, k2
    vpor ymm6, ymm0, ymm1
    vmovdqu8 ymm0 {k1}, ymm6

    vpand ymm0, ymm0, ymm4

    dec r8
    jnz .start

    vmovdqu [rcx], ymm0
    vzeroall
    ret

