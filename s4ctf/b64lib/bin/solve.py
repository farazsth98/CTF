#!/usr/bin/env python3

from pwn import *
from base64 import b64encode, b64decode

elf = ELF("./chall")
libc = ELF("./libc.so.6")
p = process(["./ld-2.27.so", "--library-path", "./", "./chall"])
#p = remote("185.14.184.242", 9990)

def encode(data):
    p.sendlineafter("> ", "1")
    p.sendafter(": ", data)

def decode(data):
    p.sendlineafter("> ", "2")
    p.sendafter(": ", data)

gdbscript = """

#b *$_base("chall")+0xab7
#b *$_base("chall")+0xad4

#b *$_base("libbase64")+0xa05
#b *$_base("libbase64")+0x800

"""

gdb.attach(p, gdbscript=gdbscript)

encode(b"\x80\x80\x80\x80")

p.interactive()
