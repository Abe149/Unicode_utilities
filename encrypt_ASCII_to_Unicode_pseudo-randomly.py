#!/usr/bin/env python3

from random import getrandbits, randrange
from sys    import stdin, stdout

### singles: dict [map] from {strings of length 3} to string of possible replacement char.s

### doubles: dict [map] from {strings of length 2} to list of string

### triples: dict [map] from {strings of length 1} to list of string

triples={}
doubles={"  ": ["  ", "　"]}
singles={' ': " ",  ### ASCII space ⇒ NBSP
         'A': "АΑ", ### first Cyrillic, then Greek
         'B': "ВΒ", ### first Cyrillic, then Greek
         'C': 'С',  ### just  Cyrillic for now —— a Roman numeral char. should probably be added later
         # 'D': '' ### a Roman numeral char. should probably be added later
         'E': "ЕΕ", ### first Cyrillic, then Greek
         'F': 'Ϝ',  ### just Greek
         'H': "НΗ", ### first Cyrillic, then Greek
         'I': "ІΙ", ### first Cyrillic, then Greek
         'K': 'Κ',  ### just the Greek, because the Cyrillic equivalent looks a _little_ bit different sometimes [a curvy termination of the upper-right stroke]
         'M': "МΜ", ### first Cyrillic, then Greek
         'N': 'Ν',  ### just Greek
         'O': "ОΟ", ### first Cyrillic, then Greek
         'P': "РΡ", ### first Cyrillic, then Greek
         'T': "ТΤ", ### first Cyrillic, then Greek
         'X': "ХΧ", ### first Cyrillic, then Greek
         'Z': 'Ζ',  ### just Greek
         'a': 'а',  ### just Cyrillic
         'c': 'с',  ### just Cyrillic
         'e': 'е',  ### just Cyrillic
         'i': 'і',  ### just Cyrillic
         'j': 'ј',  ### just Cyrillic
         'o': "оο", ### first Cyrillic, then Greek
         'p': 'р',  ### just Cyrillic [b/c the lower-case letter rho often looks “rounder” on its top-left than an English lower-case P or a Cyrillic lower-case ehr
         'x': 'х',  ### just Cyrillic
         'y': 'у',  ### just Cyrillic


         # '~': '〜' ### disabled b/c the replacement looks to be “fullwidth”, at least in iTerm2 3.1.7 using 18-point Monaco on MOSX 10.11.6
        }


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




    while len(input_line) and (input_line[:2] in doubles):
      choices_list = doubles[ input_line[:2] ]
      if len(choices_list) == 1:
        output_line += choices_list[0]
      else:
        output_line += choices_list[randrange( len(choices_list) )]

      input_line = input_line[2:]



    while len(input_line) and (input_line[0] in singles):
      choices_str = singles[ input_line[0] ]
      if len(choices_str) == 1:
        output_line += choices_str[0]
      else:
        output_line += choices_str[randrange( len(choices_str) )]

      input_line = input_line[1:]
          


    if len(input_line):
      ### nothing left that we know how to “encrypt” at the current starting position
      output_line += input_line[0]
      input_line = input_line[1:]

  print (output_line, end="")
  
  
