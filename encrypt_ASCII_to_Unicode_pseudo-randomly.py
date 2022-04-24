#!/usr/bin/env python3

from random import getrandbits
from sys    import stdin, stdout

triples={"...": '…'}
doubles={}
# doubles={"": ''} ### place-holder
# singles={"": ''} ### place-holder
singles={}



add_spacing_to_try_to_make_multiLines_text_still_line_up = True ### WIP: hard-coded

for input_line in stdin.readlines():
  ### print ("DEBUG: “"+input_line+"”")

  output_line=""
  while len(input_line):

    while (len(input_line) > 2) and (input_line[:3] in triples):
      output_line += triples[ input_line[:3] ]
      input_line = input_line[3:]
      if add_spacing_to_try_to_make_multiLines_text_still_line_up:
        output_line += "  " if getrandbits(1) else "　" ### either two NBSPs in a row or a single ideographic space

    while (len(input_line) > 1) and (input_line[:2] in doubles):
      output_line += doubles[ input_line[:2] ]
      input_line = input_line[2:]
      if add_spacing_to_try_to_make_multiLines_text_still_line_up:
        output_line += " " ### one NBSP
          
    while len(input_line) and (input_line[0] in singles):
      output_line += singles[ input_line[0] ]
      input_line = input_line[1:]
          
    if len(input_line):
      ### nothing left that we know how to “encrypt” at the current starting position
      output_line += input_line[0]
      input_line = input_line[1:]

  print (output_line)     
  
  
