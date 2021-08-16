extern _printf
extern _gets
SECTION .data
    msg     db      'Nhap chuoi: ', 0h
    format	db		'%s', 0
SECTION .bss
    input   resb    100   
SECTION .text
    global  _main
_main:
    push    msg
    push	format
    call    _printf
    add     esp, 8

    push	input
    call	_gets
    add		esp, 4

    push 	input
    push	format
    call 	_printf
    add		esp, 8
    ret