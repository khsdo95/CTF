#!/usr/bin/python
from pwn import *
from sys import argv, stdout
from socket import socket

from OpenSSL.SSL import TLSv1_METHOD, Context, Connection


def main():
    """
    Connect to an SNI-enabled server and request a specific hostname, specified
    by argv[1], of it.
    """
    if len(argv) < 2:
        print 'Usage: %s <hostname>' % (argv[0],)
        return 1

    client = socket()

    print 'Connecting...',
    stdout.flush()
    client.connect(('127.0.0.1', 51015))
    print 'connected', client.getpeername()

    client_ssl = Connection(Context(TLSv1_METHOD), client)
    client_ssl.set_connect_state()
    client_ssl.set_tlsext_host_name(argv[1])
    client_ssl.do_handshake()
    print 'Server subject is', client_ssl.get_peer_certificate().get_subject()
    client_ssl.close()


if __name__ == '__main__':
    main()

