#!/usr/bin/env python3

from random import getrandbits, randrange
from sys    import stdin, stdout



### WIP: hard-coded flags, for now
OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_as_the_original = False
OK_to_use_Unicode_chars_that_are_narrower_than_the_original_in_a_monospaced_context = False ### the mappings` destinations should have spaces in them to make up the difference
OK_to_use_Unicode_chars_that_are_wider_than_the_original    = False
add_spacing_to_try_to_make_multiLines_text_still_line_up    = True
we_are_in_a_monospaced_context = True



# def create_key_or_append_to_its_list_value(the_dict, the_key, the_value):
#   if not the_key in the_dict:
#     the_dict[the_key] = []
#   the_dict[the_key].append(the_value)

def create_key_or_plusEquals_to_its_value(the_dict, the_key, the_value): ### use either a string or a list_of_strings for “the_value”
  if not the_key in the_dict:
    the_dict[the_key] = []
  the_dict[the_key] += the_value



### singles: dict [map] from {strings of length 3} to string of possible replacement char.s

### doubles: dict [map] from {strings of length 2} to list of string

### triples: dict [map] from {strings of length 1} to list of string

triples={}
doubles={"  ": ["  ", "　"]}
singles={' ': " ",   ### ASCII space ⇒ NBSP
         ',': '‚',   ### single low-9 quotation symbol
         '-': '‑',   ### non-breaking hyphen
         '.': '․',   ### one-dot leader
         ';': ';',   ### Greek question symbol
         'A': "АΑ",  ### first Cyrillic, then Greek
         'B': "ВΒ",  ### first Cyrillic, then Greek
         'C': 'СⅭ',  ### first Cyrillic, then Roman
         'D': 'Ⅾ',   ### just Roman
         'E': "ЕΕ",  ### first Cyrillic, then Greek
         'F': 'Ϝ',   ### just Greek
         'H': "НΗ",  ### first Cyrillic, then Greek
         'I': "ІΙⅠ", ### first Cyrillic, then Greek, then Roman
         'K': 'Κ',   ### just the Greek, because the Cyrillic equivalent looks a _little_ bit different sometimes [a curvy termination of the upper-right stroke]
         'L': 'Ⅼ',   ### just Roman
         'M': "МΜⅯ", ### first Cyrillic, then Greek, then Roman
         'N': 'Ν',   ### just Greek
         'O': "ОΟ",  ### first Cyrillic, then Greek
         'P': "РΡ",  ### first Cyrillic, then Greek
         'S': 'Ѕ',   ### just Cyrillic
         'T': "ТΤ",  ### first Cyrillic, then Greek
         'V': 'Ⅴ',   ### just Roman
         'X': "ХΧⅩ", ### first Cyrillic, then Greek, then Roman
         'Z': 'Ζ',   ### just Greek
         'a': 'а',   ### just Cyrillic
         'c': 'сⅽ',  ### first Cyrillic, then Roman
         'd': 'ⅾ',   ### just Roman
         'e': 'е',   ### just Cyrillic
         'i': 'іⅰ',  ### first Cyrillic, then Roman
         'j': 'ј',   ### just Cyrillic
         'l': 'ⅼ',   ### just Roman
         'm': 'ⅿ',   ### just Roman
         'o': "оοᴏ", ### first Cyrillic, then Greek, then “Latin” small caps
         'p': 'р',   ### just Cyrillic [b/c the lower-case letter rho often looks “rounder” on its top-left than an English lower-case P or a Cyrillic lower-case ehr
         's': 'ѕ',   ### just Cyrillic
         'v': "ⅴᴠ",  ### first Roman, then “Latin” small caps
         'w': 'ᴡ',   ### just “Latin” small caps
         'x': 'хⅹ',  ### first Cyrillic, then Roman
         'y': 'у',   ### just Cyrillic
         'z': 'ᴢ',   ### just “Latin” small caps

        }



if OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_as_the_original:
  create_key_or_plusEquals_to_its_value(singles, '*', "✽✱∗✳")
  create_key_or_plusEquals_to_its_value(singles, '-', '−') ### MINUS SIGN
  create_key_or_plusEquals_to_its_value(singles, '5', "Ƽ") ### “Latin” capital “letter” tone five
  create_key_or_plusEquals_to_its_value(singles, 'c', 'ᴄ') ### small-caps ‘c’: at least sometimes has a different serif on the upper curve terminus



if OK_to_use_Unicode_chars_that_are_narrower_than_the_original_in_a_monospaced_context:
  padding = ' ' if are_we_in_a_monospaced_context else ""
  create_key_or_plusEquals_to_its_value(doubles, "!!", ["‼"+padding]) ### DOUBLE EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(doubles, "??", ["⁇"+padding]) ### DOUBLE QUESTION MARK
  create_key_or_plusEquals_to_its_value(doubles, "?!", ["⁈"+padding]) ### QUESTION EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(doubles, "!?", ["⁉"+padding]) ### EXCLAMATION QUESTION MARK
  create_key_or_plusEquals_to_its_value(doubles, "Rs", ["₨"+padding]) ### RUPEE SIGN
  create_key_or_plusEquals_to_its_value(doubles, "DZ", ["Ǳ"+padding]) ### LATIN CAPITAL LETTER DZ
  create_key_or_plusEquals_to_its_value(doubles, "Dz", ["ǲ"+padding]) ### LATIN CAPITAL LETTER D WITH SMALL LETTER Z
  create_key_or_plusEquals_to_its_value(doubles, "dz", ["ǳ"+padding]) ### LATIN SMALL LETTER DZ
# create_key_or_plusEquals_to_its_value(doubles, "__", ["_"+padding])



if OK_to_use_Unicode_chars_that_are_wider_than_the_original:
  create_key_or_plusEquals_to_its_value(singles, '~', '〜') ### WAVE DASH: not in the default/main/primary set for singles b/c the replacement looks to be “fullwidth”, at least in iTerm2 3.1.7 using 18-point Monaco on MOSX 10.11.6

  create_key_or_plusEquals_to_its_value(singles, '=', '゠') ### DIGRAM FOR GREATER YANG

  create_key_or_plusEquals_to_its_value(singles, ',', '﹐') ### SMALL COMMA
  create_key_or_plusEquals_to_its_value(singles, '.', '﹒') ### SMALL FULL STOP
  create_key_or_plusEquals_to_its_value(singles, ';', '﹔') ### SMALL SEMICOLON
  create_key_or_plusEquals_to_its_value(singles, ':', '﹕') ### SMALL COLON
  create_key_or_plusEquals_to_its_value(singles, '?', '﹖') ### SMALL QUESTION MARK
  create_key_or_plusEquals_to_its_value(singles, '!', '﹗') ### SMALL EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(singles, '(', '﹙') ### SMALL LEFT  PARENTHESIS
  create_key_or_plusEquals_to_its_value(singles, ')', '﹚') ### SMALL RIGHT PARENTHESIS
  create_key_or_plusEquals_to_its_value(singles, '{', '﹛') ### SMALL LEFT  CURLY BRACKET
  create_key_or_plusEquals_to_its_value(singles, '}', '﹜') ### SMALL RIGHT CURLY BRACKET
  create_key_or_plusEquals_to_its_value(singles, '#', '﹟') ### SMALL NUMBER SIGN
  create_key_or_plusEquals_to_its_value(singles, '&', '﹠') ### SMALL AMPERSAND
  create_key_or_plusEquals_to_its_value(singles, '*', '﹡') ### SMALL ASTERISK
  create_key_or_plusEquals_to_its_value(singles, '+', '﹢') ### SMALL PLUS SIGN
  create_key_or_plusEquals_to_its_value(singles, '-', '﹣') ### SMALL HYPHEN-MINUS
  create_key_or_plusEquals_to_its_value(singles, '<', '﹤') ### SMALL    LESS-THAN SIGN
  create_key_or_plusEquals_to_its_value(singles, '>', '﹥') ### SMALL GREATER-THAN SIGN
  create_key_or_plusEquals_to_its_value(singles, '=', '﹦') ### SMALL EQUALS SIGN
  create_key_or_plusEquals_to_its_value(singles, '$', '﹩') ### SMALL DOLLAR SIGN
  create_key_or_plusEquals_to_its_value(singles, '%', '﹪') ### SMALL PERCENT SIGN
  create_key_or_plusEquals_to_its_value(singles, '@', '﹫') ### SMALL COMMERCIAL AT

  for c in range(33, 127): ### fullwidth replacements for almost all the ASCII printables [the Unicode committee left out space in this range]
    create_key_or_plusEquals_to_its_value( singles, chr(ord('！')-ord('!')+a) )



if not we_are_in_a_monospaced_context:
  create_key_or_plusEquals_to_its_value(triples, "Pts", '₧') ### peseta(s) sign

  create_key_or_plusEquals_to_its_value(doubles, "==", '⩵')  ### TWO   CONSECUTIVE EQUALS SIGNS
  create_key_or_plusEquals_to_its_value(triples, "===", '⩶') ### THREE CONSECUTIVE EQUALS SIGNS



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
  
  
