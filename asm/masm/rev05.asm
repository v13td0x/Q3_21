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
    
.DATA
    msg             db      "Nhap chuoi: ", 0
    input           db      200     dup(?)
.CODE
    start:
            invoke StdOut, offset msg
            invoke StdIn, offset input, 200
            invoke StdOut, offset input
            invoke ExitProcess, NULL        
    End start