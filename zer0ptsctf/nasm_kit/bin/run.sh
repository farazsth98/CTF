#!/bin/sh

nasm -fbin ../exploit.S -o exploit.bin
LD_PRELOAD=./libunicorn.so.1 ./x64-emulator ./exploit.bin
