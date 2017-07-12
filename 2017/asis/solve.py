#!/usr/bin/python
from pwn import *

p = process('./start')

gdb.attach(p)

p.interactive()
