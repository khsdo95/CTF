#!/usr/bin/python
from pwn import *
from subprocess import *
import sys

res = 'SCTF{D0_U_KNoW_fUnc10N4L_L4n9U4g3'
st = 'abcdefghijklmnopqrstuvwxyzABCEDFGHIJKLMNOPQRSTUVWXYZ0123456789_{}?'
flag = '=ze=/<fQCGSNVzfDnlk$&?N3oxQp)K/CVzpznK?NeYPx0sz5'

#if len(sys.argv) > 1:
#  res = res + sys.argv[1]

for c in st:
  s = res + c
  os.system('cp ./EasyHaskell ' + s)
  out = check_output('./' + s)
  out = out.replace('\"', '')
  out = out.replace('\n', '')
  #print "data : ", s, "res : ", out
  m = len(s) % 3
  if m == 0:
    m = 0
  else:
    m = -4 + m
    out = out[:m]
  #print out[:m]
  
  if flag.startswith(out):
    print s


