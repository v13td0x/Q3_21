; https://gist.github.com/rverton/a44fc8ca67ab9ec32089
extern _printf,_gets
extern _strlen

SECTION .data
    msg     db      'Enter key: ', 0h
    msg1    db      "Enter plaintext: ", 0h
    formatS	db		'%s', 0
    formatH db      '%X ', 0
    formatI db      '%d', 0

SECTION .text
    global  _main
_main:
%assign         key         104
%assign         plainT      208
%assign         cipherT     312
    push    ebp
    mov     ebp, esp
    sub     esp, 138h       ; resever 312 bytes

    ; printf('%s', msg)
    push    msg
    push	formatS
    call    _printf
    add     esp, 8

    ; scanf('%s', &key)
    lea 	eax, dword [ebp-key]
    push    eax
    call	_gets
    add		esp, 4
    
    ; printf('%s', msg1)
    push    msg1
    push    formatS
    call    _printf
    add     esp, 8

    lea     eax, dword [ebp-plainT]
    push    eax
    call    _gets
    add     esp, 4

    ; RC4(key, plainT, cipherT)
    lea     ebx, dword[ebp-cipherT]
    push    ebx
    lea     ebx, dword[ebp-plainT]
    push    ebx
    lea     ebx, dword[ebp-key]
    push    ebx
    call    RC4
    add     esp, 8
    pop     edx
    
    L03:
        xor     ebx, ebx
        mov     bl, byte[edx]
        push    edx  
        push    ebx
        push    formatH
        call    _printf
        add     esp, 8
        pop     edx

        cmp     edi, edx
        je      finish
        inc     edx
        jmp     L03
    finish:
    mov esp, ebp
    pop ebp
    ret
;__________________________________
; void RC4(char *key, char *plainT, unsigned char *cipherT)

RC4:
%assign     S   256
    push    ebp
    mov     ebp, esp
    sub     esp, 100h           ; resever for S array type char

    ;push    dword [ebp+12]
    ;push    formatS
    ;call    _printf
    ;add     esp, 8

    ;push    dword [ebp+8]
    ;push    formatS
    ;call    _printf
    ;add     esp, 8

    ; KSA(key, S)
    lea     ebx, dword[ebp-S]
    push    ebx
    push    dword[ebp+8]
    call    KSA
    add     esp, 8

    ; PRGA(S, plainT, cipherT)
    push    dword[ebp+16]
    push    dword[ebp+12]
    lea     ebx, dword[ebp-S]
    push    ebx
    call    PRGA
    add     esp, 12

    mov esp, ebp
    pop ebp
    ret
;__________________________________
;void swap(S, j, i)

swap:
    push    ebp
    mov     ebp, esp

    push    eax
    push    ebx
    push    edi

    mov     eax, dword[ebp+8]           ; S
    add     eax, dword[ebp+16]          ; S[i]

    mov     dl, byte[eax]               ; dl <- S[i]- last 2 byte = 0

    mov     ebx, dword[ebp+8]
    add     ebx, dword[ebp+12]          ; S[j]

    mov     dh, byte[ebx]               ; 3rd and 4th byte
    mov     byte[eax], dh
    mov     byte[ebx], dl

    pop     edi
    pop     ebx
    pop     eax

    mov esp, ebp
    pop ebp
    ret
;__________________________________
;void KSA(char *key, unsigned char *S)
KSA:
    push    ebp
    mov     ebp, esp
    sub     esp, 12                     ; resever for int*3 

    push    dword[ebp+8]
    call    _strlen
    add     esp, 4
    mov     dword[ebp-4], eax           ; len(key)

    mov     edi, dword[ebp+12]
    mov     ecx, 256
    mov     al, 0
    L0:
        mov     [edi], al
        add     al, 1
        inc     edi
        loop    L0

    mov     [edi], byte 0


    mov     ecx, 256
    mov     dword[ebp-12], 0            ; i
    mov     dword[ebp-8], 0             ; j   
    L01:
        cmp     dword[ebp-12], ecx
        je      endL01

        ; jnew(*key, *S, len, *j, i)
        push    dword[ebp-12]
        lea     edi, dword[ebp-8]
        push    edi
        push    dword[ebp-4]
        push    dword[ebp+12]
        push    dword[ebp+8]
        call    jnew                    ; update dword[ebp-8]
        add     esp, 20

        ; swap(S, j, i)
        push    dword[ebp-12]
        push    dword[ebp-8]
        push    dword[ebp+12]
        call    swap
        add     esp, 12


        nextL01:
            add     dword[ebp-12], 1
            jmp     L01
    endL01:    
    mov esp, ebp
    pop ebp
    ret
;__________________________________
; jnew(*key, *S, len, *j, i )
jnew:
    push    ebp
    mov     ebp, esp

    push    eax             ; dividend[l] ->quotient
    push    ebx
    push    edx             ; dividend[h]->remainder
    push    edi
    push    esi

    ; + j
    mov     ebx, dword[ebp+20]
    mov     edi, [ebx]  
    ; + S[i]
    mov     ebx, dword[ebp+12]
    add     ebx, dword[ebp+24]
    xor     eax, eax
    mov     al, byte[ebx]
    add     edi, eax
    ; key[i % len]
    xor     eax, eax
    xor     edx, edx
    mov     eax, dword[ebp+24]
    div     dword[ebp+16]
    mov     ebx, dword[ebp+8]
    add     ebx, edx
    xor     eax, eax
    mov     al, byte[ebx]
    add     edi, eax
    ; edi % 256
    xor     eax, eax
    xor     edx, edx

    mov     eax, edi
    mov     esi, 256
    div     esi
    mov     ebx, dword[ebp+20]
    mov     [ebx], edx

    pop     esi
    pop     edi
    pop     edx
    pop     ebx
    pop     eax

    mov     esp, ebp
    pop     ebp
    ret
;__________________________________
; void PRGA(S, plainT, cipherT)
PRGA:
    push    ebp
    mov     ebp, esp
    sub     esp, 20

    mov     dword[ebp-4], 0             ; i
    mov     dword[ebp-8], 0             ; j
    mov     dword[ebp-12], 0            ; n

    push    dword[ebp+12]
    call    _strlen
    add     esp, 4

    mov     ecx, eax
    mov     esi, 256
    L02:
        ; i = (i+1) % 256
        add     dword[ebp-4], 1
        mov     eax, dword[ebp-4]
        xor     edx, edx
        div     esi
        mov     dword[ebp-4], edx
        ; j = (j + S[i]) % 256
        mov     edi, dword[ebp-8]
        mov     eax, dword[ebp+8]
        add     eax, dword[ebp-4]
        xor     ebx, ebx
        mov     bl, byte[eax]
        add     edi, ebx
        mov     eax, edi
        div     esi
        mov     dword[ebp-8], edx

        ; swap(S, j, i)
        push    dword[ebp-4]
        push    dword[ebp-8]
        push    dword[ebp+8]
        call    swap
        add     esp, 12

        ; bl = S[(S[i] + S[j]) % 256]
        xor     ebx, ebx
        xor     eax, eax                ; clean eax

        ; dl <- S[i]
        mov     edi, dword[ebp+8]
        add     edi, dword[ebp-4]
        xor     edx, edx
        mov     dl, byte[edi]
        add     eax, edx

        ; dl <- S[j]
        mov     edi, dword[ebp+8]
        add     edi, dword[ebp-8]
        xor     edx, edx
        mov     dl, byte[edi]
        add     eax, edx

        div     esi
        mov     edi, dword[ebp+8]
        add     edi, edx
        mov     bl, byte[edi]

        ; cipherT[n] = bl ^ plainT[n]
        ; dl <- plainT[n]
        mov     edi, dword[ebp+12]
        add     edi, dword[ebp-12]
        xor     edx, edx
        mov     dl, byte[edi]

        xor     dl, bl

        mov     edi, dword[ebp+16]
        add     edi, dword[ebp-12]
        mov     [edi], dl

        add     dword[ebp-12], 1
        loop    L02
    mov     esp, ebp
    pop     ebp
    ret