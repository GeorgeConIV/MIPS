        nop
        add.ne  r0, r1
        addi	r0, 50
x:      dw      500
        sub     r3, r4
        subi    r3, 50
        mul     r2, r5
        muli    r2, 5
        div     r6, r7
        divi    r7, 5
shifts: 
        lsl     r0, 1
        lsr     r1, 2
        asr     r2, 3
        b.eqz   shifts

        tar     r8, r10
        mov     r9, r11
        cmp     r0, r1
        and     r0, r1 
        andi    r0, 7
        or      r0, r1
        ori     r0, 7
        xor     r0, r1 
        xori    r0, 5
        not     r0 
        bic     ar, r1
        lda     x 
        ldc     1000
        ldo     r0, r1 
        str     x 
        br      r0
        call    shifts 
        ret
        push    sp 
        pop     sp 
        inc     sp
        dec     sp
        syscall
