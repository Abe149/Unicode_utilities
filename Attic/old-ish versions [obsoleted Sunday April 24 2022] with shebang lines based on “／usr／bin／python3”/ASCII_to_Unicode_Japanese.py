#!/usr/bin/python3

from sys import stdin, stdout
for line in stdin.readlines():
  for char in line:
    o = ord(char)
    if 32 == o: ### ASCII SPACE
     stdout.write(chr(0x3000)) ### IDEOGRAPHIC SPACE
    elif 33 <= o <= 127:
      stdout.write(chr(o+0xFF01-33))
    else:
      stdout.write(chr(o))
