import hashlib

s = raw_input()
alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
for a in alphanum:
  for b in alphanum:
    for c in alphanum:
      for d in alphanum:
        for e in alphanum:
          for f in alphanum:
            for g in alphanum:
              for h in alphanum:
                h = hashlib.sha256(s + a + b + c + d + e + f + g + h).digest()
                if h[0] == '\xff' and h[1] == '\xff' and h[2] == '\xff' and ord(h[3]) > 0xef:
                  print s + a + b + c + d + e + f + g + h
                  break

