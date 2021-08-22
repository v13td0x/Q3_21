INCLUDE C:\Irvine\Irvine32.inc

buffSize = 256

XorEncrypt PROTO,
        keyN: BYTE,
        pbuf: PTR BYTE,
        buffLen: SDWORD 
.data
    msg         BYTE        "Enter the XOR key: <0-255> ", 0
    fileHandle  HANDLE      ?
    fileName    BYTE        "text.txt", 0
    buff        BYTE        256     dup(?)
    key         BYTE      1
    len         DWORD       ?
    bytesRead   DD          ?
.code
main PROC
    ; open file
    mov     edx, offset fileName
    call    OpenInputFile
    mov     fileHandle, eax

    cmp     eax, INVALID_HANDLE_VALUE
    je      _quit

    ; read file
    mov     edx, offset buff
    mov     ecx, buffSize
    call    ReadFromFile
    mov     len, eax

    mov     edx, offset msg
    call    WriteString

    call    ReadDec
    cmp     eax, 255
    jg      _quit

    mov   key, al

    INVOKE  XorEncrypt, key, ADDR buff, len

    ; close file
    mov     eax, fileHandle
    call    CloseFile
_quit:
    exit
    ret
main ENDP
;___________________________
XorEncrypt PROC USES edi ebx ecx,
        keyN: BYTE,
        pbuf: PTR BYTE,
        buffLen: SDWORD

    mov     edi, pbuf
    mov     ecx, buffLen

    L01:
        mov      ebx, [edi]
        xor      bl, keyN
        mov    [edi], bl

        

    ret
XorEncrypt ENDP
END main 
