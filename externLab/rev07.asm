extern _printf,_scanf
extern _fopen,_fread

SECTION .data
    msg     db      'Enter xor key: ', 0h
    formatS db      '%s', 0
    formatI db      '%d-', 0

    noFile  db      0Ah, "OMG! U lost my text.txt file, let't creat it and put the string u like", 0Ah, 0
    rmode   db      "r", 0
    wmode   db      "w", 0
    file    db      "text.txt", 0
    len     equ     303

SECTION .text
    global  _main
_main:
%assign         key     1
%assign         text    303
    push    ebp
    mov     ebp, esp

    xor     eax, eax

    ; fp = fopen('text.txt', 'r') 
    push    rmode
    push    file
    call    _fopen
    add     esp, 8

    sub     esp, 130h       ; resever for key + text 304 bytes

    test    eax, eax
    jz      LostFile

    ; fread(text, 1, len, eax)
    push    eax
    push    dword len
    push    dword 1
    lea     ebx, dword [ebp-text]
    push    ebx
    call    _fread
    add     esp, 16

    mov    edi, eax            ; edi <- len(text)

    ; printf('%s', msg)
    push    msg
    push    formatS
    call    _printf
    add     esp, 8

    ; scanf("%d", &key)
    lea     eax, dword[ebp-key]
    push    eax
    push    formatI
    call    _scanf
    add     esp, 8

    ; XorEncrypt(key, text, text_len)
    push    edi
    lea     ebx, dword [ebp-text]
    push    ebx
    push    dword [ebp-key]
    call    XorEncrypt
    add     esp, 12

    ; print("%s", text)
    lea     edi, dword[ebp-text]
    push    edi
    push    formatS
    call    _printf
    add     esp, 8
    ;_____________________
    jmp     Finish
LostFile:
    ; printf('%s', noFile)
    push    noFile
    push    formatS
    call    _printf
    add     esp, 8
Finish:
    mov esp, ebp
    pop ebp
ret
;_____________________
;XorEncrypt(key, text, text_len)

XorEncrypt:
    push    ebp
    mov     ebp, esp

    ;push    dword [ebp+12]
    ;push    formatS
    ;call    _printf
    ;add     esp, 8

    ;push    dword [ebp+8]
    ;push    formatI
    ;call    _printf
    ;add     esp, 8

    ;push    dword [ebp+16]
    ;push    formatI
    ;call    _printf
    ;add     esp, 8

    mov     edi, dword[ebp+12]  ; text
    mov     ecx, dword[ebp+16]
    L0:

        xor     eax, eax
        mov     al, [edi]
        xor     al, byte[ebp+8]
        mov     [edi], al

        inc     edi
        loop    L0

        ; handle some trash chars
        mov     [edi-1], byte 0
    mov esp, ebp
    pop ebp
    ret