.386
.model flat, stdcall
option casemap: none

; includes
include \masm32\include\windows.inc
include \masm32\include\user32.inc
include \masm32\include\kernel32.inc
include \masm32\include\masm32.inc

; linked libs
includelib \masm32\lib\user32.lib
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\masm32.lib
; prototype
ReadFromFile PROTO
OpenInputFile PROTO

.DATA
    fileHandle  HANDLE      ?
    fileName    BYTE        "text.txt", 0
    buff        BYTE        256     dup(?)
    len         DWORD        0
    bytesRead   DD          ?
.CODE
    start:
            mov     eax, fileHandle
            mov     edx, OFFSET buff
            mov     ecx, 256
            call    ReadFromFile
            mov     len, eax
            invoke ExitProcess, NULL
;________________
ReadFromFile PROC
    INVOKE ReadFile,
        eax, ; file handle
        edx, ; buff
        ecx, ; max bytes to read
        ADDR bytesRead, 
        0,   ; overlapped execution flag

        cmp     eax, 0
        je      L0
        mov     eax, bytesRead
        clc     ; clear carry flag
        L0:
            ret
ReadFromFile ENDP


    
    
    