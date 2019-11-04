;; 
;;  EGRE 426
;;
;;  Lab 4 Test Assignment
;;
;;  Written by Xander Will
;;

;   init
        ldc     64      ; $v0 = 0x40
        mov     r0, ar 
        ldc     514     ; $v1 = 0x1010
        lsl     ar, 3
        mov     r1, ar
        ldc     15      ; $v2 = 0xF
        mov     r2, ar
        lsl     ar, 4   ; $v3 = 0xF0
        mov     r3, ar
        ldc     256     ; used for if cond cmp
        mov     r4, ar
        lda     array   ; $a0
        mov     r5, ar
        li      r6, 5   ; $a1 = 0x5
        ldc     255
        mov     r7, ar
        lsl     ar, 8
        mov     r8, ar

;   main
loop:   cmp     r6, zr
        b.lte   end
        dec     r6
        ldo     r5, zr
        cmp     ar, r4
        b.lte   else

        asr     r0, 3
        mov     r0, ar
        or      r1, r0
        mov     r1, ar
        mov     ar, r8
        sto     r5, zr
        b       l_end

else:   lsl     r2, 2
        mov     r2, ar
        xor     r3, r2
        mov     r3, ar
        mov     ar, r8
        sto     r5, zr

l_end:  inc     r5
        inc     r5
        b       loop

end:    ldc     0   ; return
        syscall

array:  dw      257     ; 0x101
        dw      272     ; 0x110
        dw      17      ; 0x11
        dw      240     ; 0xF0
        dw      255     ; 0xFF