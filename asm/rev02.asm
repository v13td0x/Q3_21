SECTION .data
    msg     db      'Nhap chuoi: ', 0h
SECTION .bss
    input   resb    100                    ; reserve space for 100 bytes
SECTION .text
    global  _start
_start:
    ; in 'Nhap chuoi: '
    mov     eax, msg
    call    sprint

    ; nhap input
    mov     edx, 100            ; max len(input)
    mov     ecx, input          ; addr of input
    mov     ebx, 0              ; stdin
    mov     eax, 3
    int     80h

    ; process
    mov     edi, input
    call    upperS

    ; in ra input
    mov     eax, edi
    call    sprintLF
    
    ; exit
    mov     ebx, 0
    mov     eax, 1
    int     80h
;________________________
; in: edi <- addr of string
; out: edi [addr of str.upper()]

upperS:
    push    esi
    push    ecx
    push    eax

    mov     eax, edi
    call    slen
    mov     ecx, eax                    ; ecx <- len(input)
    mov     esi, 0
l00p:
    cmp     esi, ecx
    jge     Done

    mov     byte al, [edi+esi]
    cmp     al, 61h
    jl      nextL00p                    ; if(input[i] < 'a') goto nextL00p
    cmp     al, 7Ah                    
    jg      nextL00p                    ; else if(input[i] > 'z') goto nextL00p
    sub     al, 20h                     ; else input[i] - 0x20

nextL00p:
    mov     [edi+esi], al
    add     esi, 1
    jmp     l00p

Done:
    pop     eax
    pop     ecx
    pop     esi
    ret
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
; in: eax <- addr of string
; out: eax [addr of string]
; in ra chuoi + '\n'

sprintLF:
    call    sprint

    push    eax                 ; addr of string -> stack
    mov     eax, 0Ah            ; linefeed
    push    eax                 ; linefeed -> stack de lay addr point to linefeed by esp
    mov     eax, esp            ; eax <- dia chi tro toi '\n'
    call    sprint

    pop     eax                 ; eax <- '\n', esp += 1
    pop     eax                 ; eax <- addr of string, esp += 1
    ret