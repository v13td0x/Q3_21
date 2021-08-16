section .data
	msg1	db	'Nhap chuoi: ', 0h
	msg2	db	'Chuoi moi: ', 0h
section .bss
	s		resb	255
	rs		resb	255
section .text
	global _start:
_start:
	; in chuoi  msg1
	mov		eax, msg1
	call	sprint
	
	; nhap chuoi s
	mov		edx, 255
	mov		ecx, s
	mov		ebx, 0
	mov		eax, 3
	int 	80h
	
	; process
	mov		eax, s
	call	slen
	mov		ecx, eax			; ecx len(s)
	mov		esi, 0

; loop1 push cac ky tu trong chuoi vao stack
StackChar:
	mov		eax, [s+esi]  		; eax <- s[esi]
	push	eax   				
	inc		esi
	loop	StackChar
	
	; khoi tao loop2
	mov		eax, s
	call	slen
	mov		ecx, eax
	mov		esi, 0
	
; loop2 push cac ky tu tu stack -> rs
PopChar:
	pop		eax
	mov		[rs+esi], al
	inc		esi
	loop 	PopChar
	
	; in chuoi msg2
	mov		eax, msg2
	call	sprint
	
	; in chuoi rs
	mov		eax, rs
	call	sprint
	
	mov		ebx, 0
	mov		eax, 1
	int		80h
;________________________
; in: eax <- addr of string
; out: eax [len of the string]

slen:
    push    ecx
    push    ebx
    mov     ebx, eax
nextchar:
    cmp     byte[eax], 0        ; cmp with null terminating byte
    jz      finish

    inc     eax
    jmp     nextchar
finish:
    sub     eax, ebx
    pop     ebx
    pop     ecx
    ret
;________________________
; in: eax <- addr of string
; out: eax [addr of string]
; in ra chuoi

sprint:
    push    edx
    push    ecx
    push    ebx

    push    eax                 ; addr of string -> stack
    call    slen                
                                ; eax <- len(str)
    mov     edx, eax            ; edx <- len(str)
    pop     eax                 ; eax <- addr of string

    mov     ecx, eax
    mov     ebx, 1              ; stdout
    mov     eax, 4
    int     80h

    pop     ebx
    pop     ecx
    pop     edx
    ret