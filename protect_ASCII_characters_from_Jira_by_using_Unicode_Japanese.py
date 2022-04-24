#!/usr/bin/env python3

from sys import stdin, stdout
for line in stdin.readlines():
  for char in line:
    if char in "{}_*?-^~.#": ### used as a reference: <https://jira.devtools.intel.com/secure/WikiRendererHelpAction.jspa?section=texteffects>
      stdout.write(chr(ord(char)+0xFF01-33))
    else:
      stdout.write(char)
