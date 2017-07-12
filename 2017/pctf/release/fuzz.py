from pwn import *

def do_fuzz():
  i = 0
  while True:
    os.system('cat APOCNOW.GB | radamsa > input')
    f = open('./input', 'rb')
    try:
      p = process('./gameboy')
      p.send(f.read(0x8000))
      p.send('w'*100 + 'a'*100 + 's'*100 + 'd'*100 + 'u'*100 + 'j'*100 + 'i'*100 + 'k'*100)
      p.recvline()
      p.recvline()
      p.recvline()
      p.recvline()
      p.recvline()
      p.recvline()
      p.recvline()
      p.close()
      f.close()
      continue
    except:
      os.system('mv ./input ./good' + str(i))
      i += 1

do_fuzz()

