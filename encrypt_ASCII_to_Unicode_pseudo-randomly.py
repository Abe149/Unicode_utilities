#!/usr/bin/env python3

from random import getrandbits, randrange
from sys    import stdin, stdout

### singles: dict [map] from {strings of length 3} to list of {replacement string}

### doubles: dict [map] from {strings of length 2} to list of (tuple of {replacement string, number of spaces to maybe add})

### triples: dict [map] from {strings of length 1} to list of (tuple of {replacement string, number of spaces to maybe add})

triples={"...": [('…', 2)]}
doubles={}
# doubles={"": ''} ### place-holder
singles={' ': [' ']} ### ASCII space ⇒ NBSP



add_spacing_to_try_to_make_multiLines_text_still_line_up = True ### WIP: hard-coded

for input_line in stdin.readlines():
  ### print ("DEBUG: “"+input_line+"”")

  output_line=""
  while len(input_line):

#    while (len(input_line) > 2) and (input_line[:3] in triples):
#      output_line += triples[ input_line[:3] ]
#      input_line = input_line[3:]
#      if add_spacing_to_try_to_make_multiLines_text_still_line_up:
#        output_line += "  " if getrandbits(1) else "　" ### either two NBSPs in a row or a single ideographic space



#    while (len(input_line) > 1) and (input_line[:2] in doubles):
#      output_line += doubles[ input_line[:2] ]
#      input_line = input_line[2:]
#      if add_spacing_to_try_to_make_multiLines_text_still_line_up:
#        output_line += " " ### one NBSP



    while len(input_line) and (input_line[0] in singles):
      choices_list = singles[ input_line[0] ]
      if len(choices_list) == 1:
        output_line += choices_list[0]
      else:
        output_line += choices_list[randrange( len(choices_list) )]

      input_line = input_line[1:]
          


    if len(input_line):
      ### nothing left that we know how to “encrypt” at the current starting position
      output_line += input_line[0]
      input_line = input_line[1:]

  print (output_line, end="")
  
  
