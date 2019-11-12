	addi zr, 10		
	mov r0, ar	
	
	ldc 400
	mov r1, ar		
	
	add zr, zr		
	mov r2, ar		
	
l1: 
	add zr, r0		
	sto r1, r2
	
	addi r2, 2		
	mov r2, ar
	
	subi r0, 1		
	mov r0, ar		
	cmp r0, zr		
	b.ne l1


	addi zr, 9		
	mov r0, ar 		
	
qs:		
	add zr, zr		
	mov r4, ar		
	
	mov r5, ar		
	mov r6, ar		
	mov r7, ar		

	cmp r3, r0
	b.lt if
	b end

if:
	mov r6, r3		
	mov r4, r3		
	mov r5, r0		
	
	
lop1:
	nop
ilop1:
	lsl r4, 1		
	mov r2, ar		
	ldo r1, r2	
	mov r8, ar		
	
	lsl r6, 1   	
	mov r2, ar  	
	ldo r1, r2		
	mov r9, ar		
	
	cmp r8, r9
	b.gt esc1		
	cmp r4, r0
	b.gte esc1
	
	nop
	nop
	nop
	nop
	nop
	
	addi r4, 1
	mov r4, ar
	b ilop1
	
esc1:
	lsl r5, 1		
	mov r2, ar		
	ldo r1, r2
	mov r8, ar		

	lsl r6, 1		
	mov r2, ar
	ldo r1, r2
	mov r9, ar
	
	cmp r8, r9
	b.lte esc2
	
	cmp r5, zr
	dec.gte  r5
	mov.gte r5, ar
	b esc1
	
esc2:
	cmp r4, r5
	b.gte noif
	
	lsl r4, 1		
	mov r2, ar		
	ldo r1, r2	
	mov r8, ar		

	lsl r5, 1		
	mov r2, ar		
	ldo r1, r2
	mov r9, ar		
	
	mov r7, r8
	mov r8, r9
	mov r9, r7
	
	lsl r4, 1		
	mov r2, ar		
	mov ar, r8
	sto r1, r2
	
	lsl r5, 1		
	mov r2, ar		
	mov ar, r9
	sto r1, r2
	
noif:
	cmp r4, r5
	b.lt lop1
	
	lsl r6, 1
	mov r2, ar
	ldo r1, r2
	mov r7, ar		
	
	lsl r5, 1
	mov r2, ar
	ldo r1, r2
	mov r9, ar		
	
	
	lsl r6, 1
	mov r2, ar
	mov ar, r9
	sto r1, r2		
	
	lsl r5, 1
	mov r2, ar
	mov ar, r7
	sto r1, r2		
	
	cmp r5, zr
	dec.ne  r5
	cmp r5, zr
	mov r0, ar
	
	push r3
	push r0
	
	call qs
	
	pop ra
	pop r0
	pop r3
	
	addi r5, 1
	mov r3, ar
	
	push r3
	push r0
	
	call qs
	
	pop ra
	pop r0
	pop r3
end:
	ret
	
	
	
	
	
	
	
	
	
	
	