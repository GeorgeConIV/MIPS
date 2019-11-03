;; 
;;  EGRE 426
;;
;;  Lab 4 Test Assignment
;;
;;  Written by Xander Will
;;

;   init
        ldc     64      ; $v0 = 0x40
        tar     r0
        ldc     514     ; $v1 = 0x1010
        lsl     ar, 3
        tar     r1
        ldc     15      ; $v2 = 0xF
        tar     r2
        lsl     ar, 4   ; $v3 = 0xF0
        tar     r3
        ldc     256     ; used for if cond cmp
        tar     r4
        lda     array   ; $a0
        tar     r5
        ldc     5   ; $a1 = 0x5
        tar     r6
        ldc     255
        tar     r7
        lsl     ar, 8
        tar     r8

;   main
loop:   cmp     r6, rz
        b.lte   end
        dec     r6
        ldo     r5, rz
        cmp     ar, r4
        b.lte   else

        asr     r0, 3
        tar     r0
        or      r1, r0
        tar     r1
        mov     ar, r8
        sto     r5, rz
        b       l_end

else:   lsl     r2, 2
        tar     r2
        xor     r3, r2
        tar     r3
        mov     ar, r7
        sto     r5, rz

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