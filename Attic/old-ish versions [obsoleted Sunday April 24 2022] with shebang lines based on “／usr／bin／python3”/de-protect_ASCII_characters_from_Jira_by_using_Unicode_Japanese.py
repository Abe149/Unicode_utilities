#!/usr/bin/python3

from sys import stdin, stdout

ASCII_dangerousInJira_chars="{}_*?-^~.#"

Unicode_Japanese_pseudoASCII_chars=""
for char in ASCII_dangerousInJira_chars:  Unicode_Japanese_pseudoASCII_chars+=chr(ord(char)+0xFF01-33)

for line in stdin.readlines():
  for char in line:
    if char in Unicode_Japanese_pseudoASCII_chars:
      stdout.write(chr(ord(char)-0xFF01+33))
    else:
      stdout.write(char)
