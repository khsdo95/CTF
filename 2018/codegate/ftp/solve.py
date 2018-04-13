#!/usr/bin/python
from pwn import *

context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']
local = True
elf = ELF('./ftp')

if local:
  libc = ELF('/lib/i386-linux-gnu/libc.so.6')
  p = process('./ftp')
else:
  libc = ELF()
  p = remote()

def join(name, age, ID, PW):
  p.recvuntil('Choice:')
  p.sendline(p32(1))
  p.recvuntil('Name:')
  p.sendline(name)
  p.recvuntil('Age:')
  p.sendline(str(age))
  p.recvuntil('ID:')
  p.sendline(ID)
  p.recvuntil('PW:')
  p.sendline(PW)
  p.recvuntil('Join success!')

def show():
  p.recvuntil('Choice:')
  p.send(p32(2))

def login(ID, PW):
  p.recvuntil('Choice:')
  p.send(p32(3))
  p.recvuntil('id:')
  p.sendline(ID)
  p.recvuntil('pw:')
  p.sendline(PW)
  p.recvuntil('Login success!')

def down(url):
  p.recvuntil('Choice:')
  p.send(p32(5))
  p.recvuntil('URL:')
  p.sendline(url)

def secret():
  p.recvuntil('Choice:')
  p.send(p32(8))
  
if local:
  gdb.attach(p)

join('a'*10, '2'*1, 'id', 'pw')
login('id', 'pw')
show()
down('www.naver.com')


p.interactive()
