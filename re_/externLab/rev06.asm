extern _printf,_scanf

SECTION .data
    msg     db      'Enter array size: ', 0h
    formatS	db		'%s', 0
    formatI db      '%d', 0
    fmArr   db      'A[%d] = ', 0
;SECTION .bss
;    size    resd    1
;    arr     resd    100   
SECTION .text
    global  _main
_main:
%assign         size    4h
%assign         arr     194h
    push    ebp
    mov     ebp, esp
    sub     esp, 194h       ; resever for arr + size 101*4 bytes

    ; printf('%s', msg)
    push    msg
    push	formatS
    call    _printf
    add     esp, 8

    
    ; scanf('%d', &size)
    lea 	eax, dword [ebp-size]             ; ebp-size
    push    eax
    push    formatI
    call	_scanf
    add		esp, 8
    
    ; void EnterArr(int SizeArr, int arr[])
    lea     eax, dword [ebp-arr]
    push    eax
    push    dword [ebp-size]
    call    EnterArr
    add     esp, 8

    ; void FindMax(int size, int arr[])
    lea     eax, dword [ebp-arr]
    push    eax
    push    dword [ebp-size]
    call    FindMax
    add     esp, 8

    push    msg
    push    formatS
    call    _printf
    add     esp, 8

    mov esp, ebp
    pop ebp
ret
;________________________
; void EnterArr(int SizeArr, int arr[])

EnterArr:
    push    ebp
    mov     ebp, esp

    push    eax
    push    esi
    push    edi

    mov     esi, 0
    mov     edi, dword [ebp+12]

    L0:
        cmp     esi, [ebp+8]
        je      _done

        ; printf('A[%d] = ')
        push    esi
        push    fmArr
        call    _printf
        add     esp, 8

        ; scanf("%d", &arr)
        push    edi
        push    formatI
        call    _scanf
        add     esp, 8

        ;push    dword[edi-4]
        ;push    formatI
        ;call    _printf
        ;add     esp, 8

        inc     esi
        add     edi, 4
        jmp     L0 
_done:
    pop     edi
    pop     esi
    pop     eax

    mov esp, ebp
    pop ebp
    ret
;________________________

FindMax:
    push    ebp
    mov     ebp, esp

    push    edi
    push    esi
    push    ecx

    mov     ecx, 0              ; max
    mov     esi, 0
    mov     edi, dword [ebp+12]
    L1:
        cmp     esi, [ebp+8]
        je      done

        cmp     dword[edi], ecx
        jle     nextL1
        mov     ecx, dword[edi]
    nextL1:
        inc     esi
        add     edi, 4
        jmp     L1

    done:
        push    ecx
        push    formatI
        call    _printf
        add     esp, 8
    pop     ecx
    pop     esi
    pop     edi

    mov     esp, ebp
    pop     ebp
    ret