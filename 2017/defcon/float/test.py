from pwn import *

context.arch = 'amd64'
#print disasm(asm(shellcraft.amd64.linux.cat('flag')))

sc = 'xor rbx, rbx\n'
sc += 'mov cl, 4\n'
sc += 'mov al, %s\n' % hex(ord('g'))
sc += 'shl rax, cl\n'
sc += 'mov al, %s\n' % hex(ord('a'))
sc += 'shl rax, cl\n'
sc += 'mov al, %s\n' % hex(ord('l'))
sc += 'shl rax, cl\n'
sc += 'mov al, %s\n' % hex(ord('f'))
sc += 'shl rax, cl\n'
sc += 'push rax\n'
sc += 'push rbx\n'
sc += 'mov rdi, rsp\n'

print disasm(asm(sc))
