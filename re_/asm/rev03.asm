SECTION .data
    msg     db      'Nhap chuoi: ', 0h
SECTION .bss
    input   resb    300                    ; reserve space for 300 bytes
SECTION .text
    global  _start
_start:
    ; in 'Nhap chuoi: '
    mov     eax, msg
    call    sprint

    ; nhap input
    mov     edx, 300            ; len(input)
    mov     ecx, input          ; addr of input
    mov     ebx, 0              ; stdin
    mov     eax, 3
    int     80h

    ; in ra len(input)
    mov     eax, input
    call    slen                ; eax <- len(input)
    dec     eax                 ; - '\n'
    call    iprint

    ; exit
    mov     ebx, 0
    mov     eax, 1
    int     80h
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
;________________________
; in: eax <- int
; out: none
; itoa - IntToAscii

iprint:
    push    eax
    push    ecx
    push    edx
    push    esi

    mov     ecx, 0              ; counter of how many bytes to print
; day cac phan du (<10) vao stack
divideLoop:
    inc     ecx

    xor     edx, edx            ; clean edx
    mov     esi, 10
    idiv    esi                 ; eax //= 10, edi = eax % 10

    add     edx, 30h            ; convert remaint to ascii
    push    edx
    cmp     eax, 0
    jnz     divideLoop          ; if(eax != 0) goto divideLoop

; vd 1337 -> stack = [7, 3, 3, 1], ecx = 4
;                              ^
;                             esp

; print tung ki tu luu trong stack
printLoop:
    dec     ecx
    mov     eax, esp            ; mov the stack pointer into eax for printing
    call    sprint
    pop     eax                 ; eax = esp, esp += 4

    cmp     ecx, 0
    jnz     printLoop

    pop     esi
    pop     edx
    pop     ecx
    pop     eax
    ret
;________________________
; in: eax <- int
; out: eax [int]
; itoa - IntToAscii + '\n'

iprintLF:
    call    iprint

    push    eax

    mov     eax, 0Ah
    push    eax 
    mov     eax, esp
    call    sprint
    pop     eax

    pop     eax
    ret