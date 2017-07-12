import ast
import sys
import json
import os
import resource
import signal
import socket
import struct

import cffi
import prctl

'SECU[REMOVED]'

_ffi = cffi.FFI()
_ffi.cdef('void _exit(int);')
_libc = _ffi.dlopen(None)

BAN = ['__builtins__', 'eval', 'exec', 'f_', 'co_', '+', 'code']

def _exit(n=1):
    _libc._exit(n)

def read_exact(fp, n):
    buf = ''
    while len(buf) < n:
        buf2 = os.read(fp.fileno(), n)
        if not buf2:
            _exit(123)
        buf += buf2
    return buf2

def write_exact(fp, s):
    done = 0
    while done < len(s):
        written = os.write(fp.fileno(), s[done:])
        if not written:
            _exit(123)
        done += written

class SecureEvalHost(object):
    def __init__(self):
        self.host, self.child = socket.socketpair()
        self.pid = None

    def start_child(self):
        assert not self.pid
        self.pid = os.fork()
        if not self.pid:
            self._child_main()
        self.child.close()

    def kill_child(self):
        assert self.pid
        pid, status = os.waitpid(self.pid, os.WNOHANG)
        os.kill(self.pid, signal.SIGKILL)

    def do_eval(self, msg):
        result = str(eval(msg['body']))
        if len(result) > 400:
            exit()
        return {'result': result}

    def _child_main(self):
        self.host.close()
        for fd in map(int, os.listdir('/proc/self/fd')):
            if fd != self.child.fileno():
                try:
                    os.close(fd)
                except OSError:
                    pass

        resource.setrlimit(resource.RLIMIT_CPU, (1, 1))

        prctl.set_seccomp(True)
        for x in dir(prctl):
            setattr(prctl, x, None)
        del sys.modules['prctl']

        __builtins__.input = None
        __builtins__.setattr = None
        __builtins__.getattr = None

        while True:
            sz, = struct.unpack('>L', read_exact(self.child, 4))
            doc = json.loads(read_exact(self.child, sz))
            if doc['cmd'] == 'eval':
                resp = self.do_eval(doc)
            elif doc['cmd'] == 'exit':
                _exit(0)
            goobs = json.dumps(resp)
            write_exact(self.child, struct.pack('>L', len(goobs)))
            write_exact(self.child, goobs)

    def eval(self, s):
        msg = json.dumps({'cmd': 'eval', 'body': s})
        write_exact(self.host, struct.pack('>L', len(msg)))
        write_exact(self.host, msg)
        sz, = struct.unpack('>L', read_exact(self.host, 4))
        goobs = json.loads(read_exact(self.host, sz))
        return goobs['result']

def go():
    code = raw_input('''
             *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *
          |\___/|
          )     (             .              '
         =\     /=
           )===(       *
          /               |     |
         /                \       /
  _/\_/\_/\__  _/_/\_/\_/\_/\_/\_/\_/\_/\_/\_
  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |
  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |
  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  jgs|  |  |  |  |  |  |  |  |  |  |  |  |  |

>>> ''')
    attrN = 0

    _code = code.lower()
    for ban in BAN:
        if ban in _code:
            exit()

    for node in ast.walk(ast.parse(code)):
        for instance in [ast.Exec,ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Repr]:
            if isinstance(node,instance):
                print "NO HACK"
                exit()

        if isinstance(node, ast.Attribute):
            if node.attr.startswith('__'):
                print 'NO HACK'
                exit()
            attrN += 1

    if attrN > 1:
        print 'NO HACK'
        exit()

    sec = SecureEvalHost()
    sec.start_child()
    try:
        print 'start'
        print sec.eval(code)
    finally:
        sec.kill_child()

if __name__ == '__main__':
  go()

