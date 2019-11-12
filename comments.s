	addi zr, 10		// i= 10
	mov r0, ar	
	
	ldc 250
	mov r1, ar		//adr = 250
	
	add zr, zr		
	mov r2, ar		//offset = 0
	
l1: 
	add zr, r0		//stores i in mem	
	sto r1, r2
	
	addi r2, 2		//adr += 2
	mov r2, ar
	
	subi r0, 1		//i--
	mov r0, ar			
	cmp r0, zr		//while i>0
	bne l1


	addi zr, 10		//last = r0 NEED TO CHANGE THE FIRST AND LAST INITS
	mov r0, 10 		//last = 10
	
	add zr, zr		//first = r3
	mov r3, ar		//first = 0
	push r1
	push r3
	push r0
qs:	
	pop r0
	pop r3
	pop r1

nopop:	
	add zr, zr		//i = 0
	mov r4, ar		//r4 = i
	
	mov r5, ar		//r5 = j = 0
	mov r6, ar		//r6 = pivot = 0
	mov r7, ar		//r7 = temp

	cmp r3, r0
	b.lt if
	b end

if:
	mov r6, r3		//pivot = first
	mov r4, r3		//i = first
	mov r5, r0		//j = last
	
	
lop1:
	
ilop1:
	lsl r4, 1		//i*2
	mov r2, ar		//offset = i*2
	ldo r1, r2	
	mov r8, ar		//arr[offset] = r8
	
	lsl r6, 1   	//pivot*2
	mov r2, ar  	//piv_offset = pivot*2
	ldo r1, r2		
	mov r9, ar		//arr[piv_offset] = r9
	
	cmp r8, r9
	b.gt esc1		//while(arr[offset]<=arr[piv_offset] && i<last)
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
	lsl r5, 1		//j*2
	mov r2, ar		//offset
	ldo r1, r2
	mov r8, ar		//moves thing to r8 (temp var)

	lsl r6, 1		//pivot*2
	mov r2, ar
	ldo r1, r2
	mov r9, ar
	
	cmp r8, r9
	b.lte esc2
	
	subi r5, 1
	mov r5, ar
	b esc1
	
esc2:
	cmp r4, r5
	b.gte noif
	
	lsl r4, 1		//i*2
	mov r2, ar		//offset = i*2
	ldo r1, r2	
	mov r8, ar		//arr[offset] = r8

	lsl r5, 1		//j*2
	mov r2, ar		//offset
	ldo r1, r2
	mov r9, ar		//moves thing to r9 (temp var)
	
	mov r7, r8
	mov r8, r9
	mov r9, r7
	
	lsl r4, 1		//i*2
	mov r2, ar		//offset = i*2
	mov ar, r8
	sto r1, r2
	
	lsl r5, 1		//j*2
	mov r2, ar		//offset = j*2
	mov ar, r9
	sto r1, r2
	
noif:
	cmp r4, r5
	b.lt lop1
	
	lsl r6, 1
	mov r2, ar
	ldo r1, r2
	mov r7, ar		//temp = arr[piv_offset]
	
	lsl r5, 1
	mov r2, ar
	ldo r1, r2
	mov r9, ar		//arr[j_offset] = r9
	
	
	lsl r6, 1
	mov r2, ar
	mov ar, r9
	sto r1, r2		//arr[pivot] = arr[j_offset]
	
	lsl r5, 1
	mov r2, ar
	mov ar, r7
	sto r1, r2		//arr[j_offset] = temp
	
	cmp r5, zr
	dec.nz  r5		//CALLS TO QUICKSORT HERE
	mov r0, ar
	
	push r1
	push r3
	push r0
	
	call qs
	
	addi r5, 1
	mov r3, ar
	
	push r1
	push r3
	push r0
	
	call qs
	
	
end:
	ret
//r0 = last
//r1 = base addr (never changes)
//r2 = variable offset, not set
//r3 = first
//r4 = i
//r5 = j
//r6 = pivot
//r7 = temp












