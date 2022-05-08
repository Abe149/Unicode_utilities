#!/usr/bin/env python3

DEBUG = 9

from random import getrandbits, randrange
from sys    import stdin, stdout

import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("--OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original", action="store_true")

parser.add_argument("--output_all_variations_of", type=str)

args = parser.parse_args() ### sys.argv is the default input source



### WIP: hard-coded flags, for now
OK_to_use_Unicode_chars_that_are_narrower_than_the_original_in_a_monospaced_context = False ### the mappings` destinations should have spaces in them to make up the difference
OK_to_use_Unicode_chars_that_are_wider_than_the_original    = False
add_spacing_to_try_to_make_multiLines_text_still_line_up    = True
we_are_in_a_monospaced_context = True
OK_to_use_nonBMP_codepoints = False



### NON-hardcoded flags
OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original = False
if args.OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original:
  OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original = True
  if DEBUG:
    print ("DEBUG [stderr]: set “OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original” to", OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original, file = sys.stderr)


# def create_key_or_append_to_its_list_value(the_dict, the_key, the_value):
#   if not the_key in the_dict:
#     the_dict[the_key] = []
#   the_dict[the_key].append(the_value)

def create_key_or_plusEquals_to_its_value(the_dict, the_key, the_value): ### use either a string or a list_of_strings for “the_value”
  if not the_key in the_dict:
    if the_dict is singles:
      the_dict[the_key] = ""
    else:
      the_dict[the_key] = []
  the_dict[the_key] += the_value



### singles: dict [map] from {strings of length 3} to string of possible replacement char.s

### doubles: dict [map] from {strings of length 2} to list of string

### triples: dict [map] from {strings of length 1} to list of string

quads  ={}
triples={}
doubles={"  ": ["  ", "　"]}
singles={' ': ' ',    ### ASCII space ⇒ NBSP
         ',': '‚',    ### single low-9 quotation symbol
         '-': '‑',    ### non-breaking hyphen
         '.': '․',    ### one-dot leader [for search: ONE DOT LEADER]
         ':': '꞉',    ### MODIFIER LETTER COLON
         ';': ';',    ### Greek question symbol
         "'": '𐄇',    ### AEGEAN NUMBER ONE
         '"': '𐄈',    ### AEGEAN NUMBER TWO
         'A': "АΑꓮ",  ### first Cyrillic, then Greek, then LISU LETTER A
         'B': "ВΒꓐ",  ### first Cyrillic, then Greek, then LISU LETTER BA
         'C': "СⅭꓚ",  ### first Cyrillic, then Roman, then LISU LETTER CA
         'D': "Ⅾꓓ",   ### first Roman, then LISU LETTER DA
         'E': "ЕΕꓰ",  ### first Cyrillic, then Greek, then LISU LETTER E
         'F': "Ϝꓝ𐊇",  ### first Greek, then LISU LETTER TSA
         'G': 'ꓖ',    ### LISU LETTER GA
         'H': "НΗꓧ",  ### first Cyrillic, then Greek, then LISU LETTER XA
         'I': "ІΙⅠ",  ### first Cyrillic, then Greek, then Roman
         'J': 'ꓙ',    ### LISU LETTER JA
         'K': "ΚKꓗ",  ### Greek, KELVIN SIGN, then LISU LETTER KA [omitting the Cyrillic near-equivalent b/c it looks a _little_ bit different sometimes: a curvy termination of the upper-right stroke]
         'L': "Ⅼꓡ",   ### first Roman, then LISU LETTER LA
         'M': "МΜⅯ",  ### first Cyrillic, then Greek, then Roman
         'N': 'Ν',    ### just Greek
         'O': "ОΟꓳ",  ### first Cyrillic, then Greek, then LISU LETTER O
         'P': "РΡꓑ",  ### first Cyrillic, then Greek, then LISU LETTER PA
         'R': 'ꓣ',    ### LISU LETTER ZHA
         'S': "Ѕꓢ",   ### first Cyrillic, then LISU LETTER SA
         'T': "ТΤꓔ",  ### first Cyrillic, then Greek, then LISU LETTER TA
         'U': 'ꓴ',    ### LISU LETTER U
         'V': "Ⅴꓦ",   ### first Roman, then LISU LETTER ZHA
         'X': "ХΧⅩꓫ", ### first Cyrillic, then Greek, then Roman, then LISU LETTER SHA
         'Y': 'ꓬ',    ### LISU LETTER YA
         'Z': "Ζꓜ",   ### first Greek, then LISU LETTER DZA

         'a': 'а',   ### just Cyrillic
         'c': "сⅽ",  ### first Cyrillic, then Roman
         'd': "ⅾꝱ",  ### first Roman, then LATIN SMALL LETTER DUM
         'e': 'е',   ### just Cyrillic
         'i': "іⅰ",  ### first Cyrillic, then Roman
         'j': 'ј',   ### just Cyrillic
         'l': 'ⅼ',   ### just Roman
         'm': 'ⅿ',   ### just Roman
         'o': "оοᴏ", ### first Cyrillic, then Greek, then “Latin” small caps
         'p': 'р',   ### just Cyrillic [b/c the lower-case letter rho often looks “rounder” on its top-left than an English lower-case P or a Cyrillic lower-case ehr
         's': 'ѕ',   ### just Cyrillic
         'v': "ⅴᴠ",  ### first Roman, then “Latin” small caps
         'w': 'ᴡ',   ### just “Latin” small caps
         'x': "хⅹ",  ### first Cyrillic, then Roman
         'y': 'у',   ### just Cyrillic
         'z': 'ᴢ',   ### just “Latin” small caps

         '~': '∼'    ### TILDE OPERATOR
        }



if OK_to_use_nonBMP_codepoints:
  create_key_or_plusEquals_to_its_value(  singles, 'E', '𐊆')   ### LYCIAN LETTER I
  create_key_or_plusEquals_to_its_value(  singles, 'F', '𐊇')   ### LYCIAN LETTER W
  create_key_or_plusEquals_to_its_value(  singles, 'I', '𐊈')   ### LYCIAN LETTER Z



if OK_to_use_mappings_that_are_likely_to_be_visually_distinguishable_from_the_original_but_should_have_the_same_width_category_as_the_original:

  create_key_or_plusEquals_to_its_value(  singles, '#', '⋕')   ### EQUAL AND PARALLEL TO
  create_key_or_plusEquals_to_its_value(  singles, '#', '𐄹')   ### AEGEAN WEIGHT SECOND SUBUNIT
  create_key_or_plusEquals_to_its_value(  singles, '*', "✽✱∗✳⁕") ### last one as of this writing: FLOWER PUNCTUATION MARK
  create_key_or_plusEquals_to_its_value(  singles, '-', "−𐄐")  ### MINUS SIGN, AEGEAN NUMBER TEN
  create_key_or_plusEquals_to_its_value(  singles, '~', '⁓')   ### SWUNG DASH
  create_key_or_plusEquals_to_its_value(  singles, '%', '⁒')   ### COMMERCIAL MINUS SIGN

  create_key_or_plusEquals_to_its_value(  singles, '0', '𝟢')   ### MATHEMATICAL SANS-SERIF DIGIT ZERO
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '0', '𝟶')   ### MATHEMATICAL MONOSPACE  DIGIT ZERO  [for search: MATHEMATICAL MONOSPACE DIGIT ZERO]

  create_key_or_plusEquals_to_its_value(  singles, '1', '𝟣')   ### MATHEMATICAL SANS-SERIF DIGIT ONE
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '1', '𝟷')   ### MATHEMATICAL MONOSPACE  DIGIT ONE   [for search: MATHEMATICAL MONOSPACE DIGIT ONE]

  create_key_or_plusEquals_to_its_value(  singles, '2', '𝟤')   ### MATHEMATICAL SANS-SERIF DIGIT TWO
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '2', '𝟸')   ### MATHEMATICAL MONOSPACE  DIGIT TWO   [for search: MONOSPACE DIGIT TWO]

  create_key_or_plusEquals_to_its_value(  singles, '3', "𝟥З")  ### MATHEMATICAL SANS-SERIF DIGIT THREE, CYRILLIC CAPITAL LETTER ZE
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '3', '𝟹')   ### MATHEMATICAL MONOSPACE  DIGIT THREE [for search: MATHEMATICAL MONOSPACE DIGIT THREE]

  create_key_or_plusEquals_to_its_value(  singles, '4', '𝟦')   ### MATHEMATICAL SANS-SERIF DIGIT FOUR
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '4', '𝟺')   ### MATHEMATICAL MONOSPACE  DIGIT FOUR  [for search: MATHEMATICAL MONOSPACE DIGIT FOUR]

# create_key_or_plusEquals_to_its_value(  singles, '5', 'Ƽ')   ### “Latin” capital “letter” tone five ### maybe To Do: re-enable this replacement _contextually_, where neither the preceding char. nor the succeeding char. in the original was an ASCII digit [otherwise this too-often sticks out like a sore thumb]

  create_key_or_plusEquals_to_its_value(  singles, '5', '𝟧')   ### MATHEMATICAL SANS-SERIF DIGIT FIVE
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '5', '𝟻')   ### MATHEMATICAL MONOSPACE  DIGIT FIVE [for search: MATHEMATICAL MONOSPACE DIGIT FIVE]

  create_key_or_plusEquals_to_its_value(  singles, '6', '𝟨')   ### MATHEMATICAL SANS-SERIF DIGIT SIX [for search:
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '6', '𝟼')   ### MATHEMATICAL MONOSPACE  DIGIT SIX [for search: MATHEMATICAL MONOSPACE DIGIT SIX]

  create_key_or_plusEquals_to_its_value(  singles, '7', '𝟩')   ### MATHEMATICAL SANS-SERIF DIGIT SEVEN
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '7', '𝟽')   ### MATHEMATICAL MONOSPACE  DIGIT SEVEN [for search: MONOSPACE DIGIT SEVEN]

  create_key_or_plusEquals_to_its_value(  singles, '8', '𝟪')   ### MATHEMATICAL SANS-SERIF DIGIT EIGHT
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '8', '𝟾')   ### MATHEMATICAL MONOSPACE  DIGIT EIGHT [for search: MONOSPACE DIGIT EIGHT]

  create_key_or_plusEquals_to_its_value(  singles, '9', '𝟫')   ### MATHEMATICAL SANS-SERIF DIGIT NINE
  if we_are_in_a_monospaced_context:
    create_key_or_plusEquals_to_its_value(singles, '9', '𝟿')   ### MATHEMATICAL MONOSPACE  DIGIT NINE [for search: MONOSPACE DIGIT NINE]

  create_key_or_plusEquals_to_its_value(  singles, '|', "∣⎮❘") ### DIVIDES, INTEGRAL EXTENSION, LIGHT VERTICAL BAR
  create_key_or_plusEquals_to_its_value(  singles, '|', '│')   ### BOX DRAWINGS LIGHT VERTICAL
  create_key_or_plusEquals_to_its_value(  singles, '|', '┃')   ### BOX DRAWINGS HEAVY VERTICAL

  create_key_or_plusEquals_to_its_value(  singles, '=', '𐄑')   ### AEGEAN NUMBER TWENTY
  create_key_or_plusEquals_to_its_value(  singles, '=', '꞊')   ### MODIFIER LETTER SHORT EQUALS SIGN
  create_key_or_plusEquals_to_its_value(  singles, '=', '𐆐')   ### ROMAN SEXTANS SIGN
  create_key_or_plusEquals_to_its_value(  singles, '-', '𐆑')   ### ROMAN UNCIA   SIGN [for search: ROMAN UNCIA SIGN

  create_key_or_plusEquals_to_its_value(  singles, 'E', '⋿')   ### Z NOTATION BAG MEMBERSHIP
  create_key_or_plusEquals_to_its_value(  singles, 'c', 'ᴄ')   ### small-caps ‘c’: at least sometimes has a different serif on the upper curve terminus

  ### to maybe re-enable later, gated by a flag that promises that the output will be viewed in a sans-serif font
  # create_key_or_plusEquals_to_its_value(  singles, 'x', '⨉')   ### N-ARY TIMES OPERATOR

  create_key_or_plusEquals_to_its_value(  singles, '/' , '∕')  ### DIVISION SLASH
  create_key_or_plusEquals_to_its_value(  singles, '/' , '╱')  ### BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
  create_key_or_plusEquals_to_its_value(  singles, '\\', '╲')  ### BOX DRAWINGS LIGHT DIAGONAL UPPER  LEFT TO LOWER RIGHT [BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT]
  create_key_or_plusEquals_to_its_value(  singles, '\\', '∖')  ### SET MINUS
  create_key_or_plusEquals_to_its_value(  singles, '\\', '⧵')  ### REVERSE SOLIDUS OPERATOR

  create_key_or_plusEquals_to_its_value(  doubles, '((', ['｟']) ### FULLWIDTH  LEFT WHITE PARENTHESIS [for search: FULLWIDTH LEFT WHITE PARENTHESIS]
  create_key_or_plusEquals_to_its_value(  doubles, '))', ['｠']) ### FULLWIDTH RIGHT WHITE PARENTHESIS
  create_key_or_plusEquals_to_its_value(  doubles, "<<", ['《']) ###  LEFT DOUBLE ANGLE BRACKET
  create_key_or_plusEquals_to_its_value(  doubles, ">>", ['》']) ### RIGHT DOUBLE ANGLE BRACKET

  create_key_or_plusEquals_to_its_value(singles, '(', '❨') ### MEDIUM  LEFT PARENTHESIS ORNAMENT [for search: MEDIUM LEFT PARENTHESIS ORNAMENT]
  create_key_or_plusEquals_to_its_value(singles, ')', '❩') ### MEDIUM RIGHT PARENTHESIS ORNAMENT
  create_key_or_plusEquals_to_its_value(singles, '<', '❮') ### HEAVY  LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT [HEAVY LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT]
  create_key_or_plusEquals_to_its_value(singles, '>', '❯') ### HEAVY RIGHT-POINTING ANGLE QUOTATION MARK ORNAMENT

  create_key_or_plusEquals_to_its_value(singles, '{', '❴') ### MEDIUM  LEFT CURLY BRACKET ORNAMENT [for search: MEDIUM LEFT CURLY BRACKET ORNAMENT]
  create_key_or_plusEquals_to_its_value(singles, '}', '❵') ### MEDIUM RIGHT CURLY BRACKET ORNAMENT

  create_key_or_plusEquals_to_its_value(doubles, "da", ['㍲']) ### SQUARE DA
  create_key_or_plusEquals_to_its_value(doubles, "AU", ['㍳']) ### SQUARE AU
  create_key_or_plusEquals_to_its_value(doubles, "oV", ['㍵']) ### SQUARE OV
  create_key_or_plusEquals_to_its_value(doubles, "pc", ['㍶']) ### SQUARE PC

  create_key_or_plusEquals_to_its_value(doubles, "pA", ['㎀']) ### SQUARE PA AMPS
  create_key_or_plusEquals_to_its_value(doubles, "nA", ['㎁']) ### SQUARE NA
  create_key_or_plusEquals_to_its_value(doubles, "mA", ['㎃']) ### SQUARE MA
  create_key_or_plusEquals_to_its_value(doubles, "kA", ['㎄']) ### SQUARE KA ### should I disable this one?  At least on font on MOSX 10.11.6 on my primary MBP incorectly has this looking like “KA”

  create_key_or_plusEquals_to_its_value(doubles, "KB", ['㎅']) ### SQUARE KB
  create_key_or_plusEquals_to_its_value(doubles, "MB", ['㎆']) ### SQUARE MB
  create_key_or_plusEquals_to_its_value(doubles, "GB", ['㎇']) ### SQUARE GB

  create_key_or_plusEquals_to_its_value(doubles, "pF", ['㎊']) ### SQUARE PF
  create_key_or_plusEquals_to_its_value(doubles, "nF", ['㎋']) ### SQUARE NF

  create_key_or_plusEquals_to_its_value(doubles, "mg", ['㎎']) ### SQUARE MG
  create_key_or_plusEquals_to_its_value(doubles, "kg", ['㎏']) ### SQUARE KG

  create_key_or_plusEquals_to_its_value(doubles, "Hz", ['㎐']) ### SQUARE HZ

  create_key_or_plusEquals_to_its_value(doubles, "fm", ['㎙']) ### SQUARE FM
  create_key_or_plusEquals_to_its_value(doubles, "nm", ['㎚']) ### SQUARE NM
  create_key_or_plusEquals_to_its_value(doubles, "mm", ['㎜']) ### SQUARE MM
  create_key_or_plusEquals_to_its_value(doubles, "cm", ['㎝']) ### SQUARE CM
  create_key_or_plusEquals_to_its_value(doubles, "km", ['㎞']) ### SQUARE KM

  create_key_or_plusEquals_to_its_value(doubles, "ps", ['㎰']) ### SQUARE PS
  create_key_or_plusEquals_to_its_value(doubles, "ns", ['㎱']) ### SQUARE NS
  create_key_or_plusEquals_to_its_value(doubles, "ms", ['㎳']) ### SQUARE MS

  create_key_or_plusEquals_to_its_value(doubles, "Pa", ['㎩']) ### SQUARE PA

  create_key_or_plusEquals_to_its_value(doubles, "pV", ['㎴']) ### SQUARE pV
  create_key_or_plusEquals_to_its_value(doubles, "nV", ['㎵']) ### SQUARE nV
  create_key_or_plusEquals_to_its_value(doubles, "mV", ['㎷']) ### SQUARE nV
  create_key_or_plusEquals_to_its_value(doubles, "kV", ['㎸']) ### SQUARE KV ### should I disable this one?  At least on font on MOSX 10.11.6 on my primary MBP incorectly has this looking like “KV”
  create_key_or_plusEquals_to_its_value(doubles, "MV", ['㎹']) ### SQUARE MV

  create_key_or_plusEquals_to_its_value(doubles, "pW", ['㎺']) ### SQUARE pW
  create_key_or_plusEquals_to_its_value(doubles, "nW", ['㎻']) ### SQUARE nW
  create_key_or_plusEquals_to_its_value(doubles, "mW", ['㎽']) ### SQUARE nW
  create_key_or_plusEquals_to_its_value(doubles, "kW", ['㎾']) ### SQUARE KW ### should I disable this one?  At least on font on MOSX 10.11.6 on my primary MBP incorectly has this looking like “KV”
  create_key_or_plusEquals_to_its_value(doubles, "MW", ['㎿']) ### SQUARE MW

  create_key_or_plusEquals_to_its_value(doubles, "Bq", ['㏃']) ### SQUARE BQ
  create_key_or_plusEquals_to_its_value(doubles, "cc", ['㏄']) ### SQUARE CC
  create_key_or_plusEquals_to_its_value(doubles, "cd", ['㏅']) ### SQUARE CD

  create_key_or_plusEquals_to_its_value(doubles, "dB", ['㏈']) ### SQUARE DB
  create_key_or_plusEquals_to_its_value(doubles, "Gy", ['㏉']) ### SQUARE GY
  create_key_or_plusEquals_to_its_value(doubles, "ha", ['㏊']) ### SQUARE HA
  create_key_or_plusEquals_to_its_value(doubles, "in", ['㏌']) ### SQUARE IN
  create_key_or_plusEquals_to_its_value(doubles, "KM", ['㏎']) ### SQUARE KM CAPITAL
  create_key_or_plusEquals_to_its_value(doubles, "kt", ['㏏']) ### SQUARE KT
  create_key_or_plusEquals_to_its_value(doubles, "lm", ['㏐']) ### SQUARE LM
  create_key_or_plusEquals_to_its_value(doubles, "ln", ['㏑']) ### SQUARE LN
  create_key_or_plusEquals_to_its_value(doubles, "lx", ['㏓']) ### SQUARE LX
  create_key_or_plusEquals_to_its_value(doubles, "mb", ['㏔']) ### SQUARE MB SMALL
  create_key_or_plusEquals_to_its_value(doubles, "pH", ['㏗']) ### SQUARE PH
  create_key_or_plusEquals_to_its_value(doubles, "PR", ['㏚']) ### SQUARE PR
  create_key_or_plusEquals_to_its_value(doubles, "sr", ['㏛']) ### SQUARE SR
  create_key_or_plusEquals_to_its_value(doubles, "Sv", ['㏜']) ### SQUARE SV
  create_key_or_plusEquals_to_its_value(doubles, "wb", ['㏝']) ### SQUARE WB

  create_key_or_plusEquals_to_its_value(singles, 's', 'ꜱ')     ### LATIN LETTER SMALL CAPITAL S [moved to the “ghetto” b/c it is forcing a serif view in iTerm2 on my MBP running 10.11.6]

# create_key_or_plusEquals_to_its_value(singles, '_', '_') ###
# create_key_or_plusEquals_to_its_value(doubles, "__", ['_']) ###



if OK_to_use_Unicode_chars_that_are_narrower_than_the_original_in_a_monospaced_context:

  padding = ' ' if are_we_in_a_monospaced_context else ""

  create_key_or_plusEquals_to_its_value(doubles, "!!", ['‼'+padding]) ### DOUBLE EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(doubles, "??", ['⁇'+padding]) ### DOUBLE QUESTION MARK
  create_key_or_plusEquals_to_its_value(doubles, "?!", ['⁈'+padding]) ### QUESTION EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(doubles, "!?", ['⁉'+padding]) ### EXCLAMATION QUESTION MARK
  create_key_or_plusEquals_to_its_value(doubles, "--", ['╌'+padding]) ### BOX DRAWINGS LIGHT DOUBLE DASH HORIZONTAL
  create_key_or_plusEquals_to_its_value(doubles, "--", ['╍'+padding]) ### BOX DRAWINGS HEAVY DOUBLE DASH HORIZONTAL
  create_key_or_plusEquals_to_its_value(doubles, "==", ['𐄓'+padding, '⩵'+padding]) ### AEGEAN NUMBER FORTY, TWO CONSECUTIVE EQUALS SIGNS

  create_key_or_plusEquals_to_its_value(doubles, "((", ['⸨'+padding]) ###  LEFT DOUBLE PARENTHESIS
  create_key_or_plusEquals_to_its_value(doubles, "))", ['⸩'+padding]) ### RIGHT DOUBLE PARENTHESIS

  create_key_or_plusEquals_to_its_value(doubles, "DZ", ['Ǳ'+padding]) ### LATIN CAPITAL LETTER DZ
  create_key_or_plusEquals_to_its_value(doubles, "Dz", ['ǲ'+padding]) ### LATIN CAPITAL LETTER D WITH SMALL LETTER Z
  create_key_or_plusEquals_to_its_value(doubles, "dz", ['ǳ'+padding]) ### LATIN SMALL LETTER DZ

  create_key_or_plusEquals_to_its_value(doubles, "II", ['Ⅱ'+padding]) ###       ROMAN NUMERAL TWO
  create_key_or_plusEquals_to_its_value(doubles, "ii", ['ⅱ'+padding]) ### SMALL ROMAN NUMERAL TWO

  create_key_or_plusEquals_to_its_value(doubles, "IV", ['Ⅳ'+padding]) ###       ROMAN NUMERAL FOUR
  create_key_or_plusEquals_to_its_value(doubles, "iv", ['ⅳ'+padding]) ### SMALL ROMAN NUMERAL FOUR

  create_key_or_plusEquals_to_its_value(doubles, "IX", ['Ⅸ'+padding]) ###       ROMAN NUMERAL NINE
  create_key_or_plusEquals_to_its_value(doubles, "ix", ['ⅸ'+padding]) ### SMALL ROMAN NUMERAL NINE

  create_key_or_plusEquals_to_its_value(doubles, "LJ", ['Ǉ'+padding]) ### LATIN CAPITAL LETTER LJ
  create_key_or_plusEquals_to_its_value(doubles, "Lj", ['ǈ'+padding]) ### LATIN CAPITAL LETTER L WITH SMALL LETTER J
  create_key_or_plusEquals_to_its_value(doubles, "lj", ['ǉ'+padding]) ### LATIN SMALL LETTER LJ

  create_key_or_plusEquals_to_its_value(doubles, "NJ", ['Ǌ'+padding]) ### LATIN CAPITAL LETTER NJ
  create_key_or_plusEquals_to_its_value(doubles, "Nj", ['ǋ'+padding]) ### LATIN CAPITAL LETTER N WITH SMALL LETTER J
  create_key_or_plusEquals_to_its_value(doubles, "nj", ['ǌ'+padding]) ### LATIN SMALL LETTER NJ

  create_key_or_plusEquals_to_its_value(doubles, "Rs", ['₨'+padding]) ### RUPEE SIGN

  create_key_or_plusEquals_to_its_value(doubles, "VI", ['Ⅵ'+padding]) ###       ROMAN NUMERAL SIX
  create_key_or_plusEquals_to_its_value(doubles, "vi", ['ⅵ'+padding]) ### SMALL ROMAN NUMERAL SIX

  create_key_or_plusEquals_to_its_value(doubles, "XI", ['Ⅺ'+padding]) ###       ROMAN NUMERAL ELEVEN
  create_key_or_plusEquals_to_its_value(doubles, "xi", ['ⅺ'+padding]) ### SMALL ROMAN NUMERAL ELEVEN

  create_key_or_plusEquals_to_its_value(doubles, "||", ['‖'+padding]) ### DOUBLE VERTICAL LINE
  create_key_or_plusEquals_to_its_value(doubles, "<<", ['⟪'+padding]) ### MATHEMATICAL  LEFT DOUBLE ANGLE BRACKET [MATHEMATICAL LEFT DOUBLE ANGLE BRACKET]
  create_key_or_plusEquals_to_its_value(doubles, ">>", ['⟫'+padding]) ### MATHEMATICAL RIGHT DOUBLE ANGLE BRACKET
  create_key_or_plusEquals_to_its_value(doubles, "<<", ['≪'+padding]) ### MUCH    LESS-THAN [for search: MUCH LESS-THAN]
  create_key_or_plusEquals_to_its_value(doubles, ">>", ['≫'+padding]) ### MUCH GREATER-THAN
  create_key_or_plusEquals_to_its_value(doubles, ">>", ['⨠'+padding]) ### Z NOTATION SCHEMA PIPING

  create_key_or_plusEquals_to_its_value(triples, "bar", ['㍴'+padding]) ### SQUARE BAR

  create_key_or_plusEquals_to_its_value(triples, "hPa", ['㍱'+padding]) ### SQUARE HPA
  create_key_or_plusEquals_to_its_value(triples, "kPa", ['㎪'+padding]) ### SQUARE KPA
  create_key_or_plusEquals_to_its_value(triples, "MPa", ['㎫'+padding]) ### SQUARE MPA
  create_key_or_plusEquals_to_its_value(triples, "GPa", ['㎬'+padding]) ### SQUARE GPA

  create_key_or_plusEquals_to_its_value(triples, "KHz", ['㎑'+padding]) ### SQUARE KHZ
  create_key_or_plusEquals_to_its_value(triples, "MHz", ['㎒'+padding]) ### SQUARE MHZ
  create_key_or_plusEquals_to_its_value(triples, "GHz", ['㎓'+padding]) ### SQUARE GHZ
  create_key_or_plusEquals_to_its_value(triples, "THz", ['㎔'+padding]) ### SQUARE THZ

  create_key_or_plusEquals_to_its_value(triples, "rad", ['㎭'+padding]) ### SQUARE RAD
  create_key_or_plusEquals_to_its_value(triples, "log", ['㏒'+padding]) ### SQUARE LOG
  create_key_or_plusEquals_to_its_value(triples, "mil", ['㏕'+padding]) ### SQUARE MIL
  create_key_or_plusEquals_to_its_value(triples, "mol", ['㏖'+padding]) ### SQUARE MOL
  create_key_or_plusEquals_to_its_value(triples, "PPM", ['㏙'+padding]) ### SQUARE PPM

# create_key_or_plusEquals_to_its_value(triples, "Co.", ['㏇'+padding]) ### SQUARE CO ### disabled b/c it sometimes looks like “CO.” on 10.11.6 on my main MBP

# create_key_or_plusEquals_to_its_value(doubles, "__", ['_'+padding])



if OK_to_use_Unicode_chars_that_are_wider_than_the_original:

  create_key_or_plusEquals_to_its_value(singles, '~', '〜') ### WAVE DASH: not in the default/main/primary set for singles b/c the replacement looks to be “fullwidth”, at least in iTerm2 3.1.7 using 18-point Monaco on MOSX 10.11.6

  create_key_or_plusEquals_to_its_value(singles, '=', '゠') ### DIGRAM FOR GREATER YANG

  create_key_or_plusEquals_to_its_value(singles, '<', '〈') ###  LEFT ANGLE BRACKET
  create_key_or_plusEquals_to_its_value(singles, '>', '〉') ### RIGHT ANGLE BRACKET

  create_key_or_plusEquals_to_its_value(singles, ',', '﹐') ### SMALL COMMA
  create_key_or_plusEquals_to_its_value(singles, '.', '﹒') ### SMALL FULL STOP
  create_key_or_plusEquals_to_its_value(singles, ';', '﹔') ### SMALL SEMICOLON
  create_key_or_plusEquals_to_its_value(singles, ':', '﹕') ### SMALL COLON
  create_key_or_plusEquals_to_its_value(singles, '?', '﹖') ### SMALL QUESTION MARK
  create_key_or_plusEquals_to_its_value(singles, '!', '﹗') ### SMALL EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(singles, '(', '﹙') ### SMALL LEFT  PARENTHESIS [for search: SMALL LEFT PARENTHESIS]
  create_key_or_plusEquals_to_its_value(singles, ')', '﹚') ### SMALL RIGHT PARENTHESIS
  create_key_or_plusEquals_to_its_value(singles, '{', '﹛') ### SMALL LEFT  CURLY BRACKET [for search: LEFT CURLY BRACKET]
  create_key_or_plusEquals_to_its_value(singles, '}', '﹜') ### SMALL RIGHT CURLY BRACKET
  create_key_or_plusEquals_to_its_value(singles, '#', '﹟') ### SMALL NUMBER SIGN
  create_key_or_plusEquals_to_its_value(singles, '&', '﹠') ### SMALL AMPERSAND
  create_key_or_plusEquals_to_its_value(singles, '*', '﹡') ### SMALL ASTERISK
  create_key_or_plusEquals_to_its_value(singles, '+', '﹢') ### SMALL PLUS SIGN
  create_key_or_plusEquals_to_its_value(singles, '-', '﹣') ### SMALL HYPHEN-MINUS
  create_key_or_plusEquals_to_its_value(singles, '<', '﹤') ### SMALL    LESS-THAN SIGN [for search: SMALL LESS-THAN SIGN]
  create_key_or_plusEquals_to_its_value(singles, '>', '﹥') ### SMALL GREATER-THAN SIGN
  create_key_or_plusEquals_to_its_value(singles, '=', '﹦') ### SMALL EQUALS SIGN
  create_key_or_plusEquals_to_its_value(singles, '$', '﹩') ### SMALL DOLLAR SIGN
  create_key_or_plusEquals_to_its_value(singles, '%', '﹪') ### SMALL PERCENT SIGN
  create_key_or_plusEquals_to_its_value(singles, '@', '﹫') ### SMALL COMMERCIAL AT

### note: BIG SOLIDUS and BIG REVERSE SOLIDUS seem to be “weird”: in Mac OS X 10.11`s character viewer [now renamed “Emoji and Symbols” :-(], they both seem to be full-width, but in both iTerm2 and TextEdit [using Times New Roman] they are _not_ [albeit in TextEdit they _are_ wider than the respective ASCII char.s]
  create_key_or_plusEquals_to_its_value(singles, '/' , '⧸') ### BIG         SOLIDUS [for search: BIG SOLIDUS]
  create_key_or_plusEquals_to_its_value(singles, '\\', '⧹') ### BIG REVERSE SOLIDUS

  create_key_or_plusEquals_to_its_value(singles, ':' , '︰') ### PRESENTATION FORM FOR VERTICAL TWO DOT LEADER
  create_key_or_plusEquals_to_its_value(singles, ':' , '︓') ### PRESENTATION FORM FOR VERTICAL     COLON [PRESENTATION FORM FOR VERTICAL COLON]
  create_key_or_plusEquals_to_its_value(singles, ';' , '︔') ### PRESENTATION FORM FOR VERTICAL SEMICOLON
  create_key_or_plusEquals_to_its_value(singles, '!' , '︕') ### PRESENTATION FORM FOR VERTICAL EXCLAMATION MARK
  create_key_or_plusEquals_to_its_value(singles, '?' , '︖') ### PRESENTATION FORM FOR VERTICAL QUESTION    MARK [PRESENTATION FORM FOR VERTICAL QUESTION MARK]

  ### fullwidth replacements for almost all the ASCII printables [the Unicode committee left out space in this range]
  for c in range(33, 127):
    create_key_or_plusEquals_to_its_value( singles, chr(ord('！')-ord('!')+c) )



if not we_are_in_a_monospaced_context:
# create_key_or_plusEquals_to_its_value(singles, '_', '_') ### 
  create_key_or_plusEquals_to_its_value(singles, '+', '➕') ### HEAVY  PLUS SIGN [for search: HEAVY PLUS SIGN]
  create_key_or_plusEquals_to_its_value(singles, '-', '➖') ### HEAVY MINUS SIGN

  create_key_or_plusEquals_to_its_value(doubles, "><", ['⪥' ])  ### GREATER-THAN BESIDE LESS-THAN

  create_key_or_plusEquals_to_its_value(doubles, "==", ['⩵' ])  ### TWO   CONSECUTIVE EQUALS SIGNS [for search: TWO CONSECUTIVE EQUALS SIGNS]
  create_key_or_plusEquals_to_its_value(triples, "===", ['⩶'])  ### THREE CONSECUTIVE EQUALS SIGNS
  create_key_or_plusEquals_to_its_value(triples, "<<<", ['⋘'])  ### VERY MUCH    LESS-THAN [for search: VERY MUCH LESS-THAN]
  create_key_or_plusEquals_to_its_value(triples, ">>>", ['⋙'])  ### VERY MUCH GREATER-THAN

  create_key_or_plusEquals_to_its_value(triples, "::=", '⩴')    ###       DOUBLE COLON EQUAL
  create_key_or_plusEquals_to_its_value(doubles, "//",  ['⫽'])  ###       DOUBLE SOLIDUS OPERATOR
  create_key_or_plusEquals_to_its_value(triples, "///", ['⫻'])  ###       TRIPLE SOLIDUS BINARY RELATION
  create_key_or_plusEquals_to_its_value(triples, "|||", ['_'])  ### LARGE TRIPLE VERTICAL BAR OPERATOR

  create_key_or_plusEquals_to_its_value(triples, "(a)", ['⒜'])  ### PARENTHESIZED LATIN SMALL LETTER A
  create_key_or_plusEquals_to_its_value(triples, "(b)", ['⒝'])  ### PARENTHESIZED LATIN SMALL LETTER B
  create_key_or_plusEquals_to_its_value(triples, "(c)", ['⒞'])  ### PARENTHESIZED LATIN SMALL LETTER C
  create_key_or_plusEquals_to_its_value(triples, "(d)", ['⒟'])  ### PARENTHESIZED LATIN SMALL LETTER D
  create_key_or_plusEquals_to_its_value(triples, "(e)", ['⒠'])  ### PARENTHESIZED LATIN SMALL LETTER E
  create_key_or_plusEquals_to_its_value(triples, "(f)", ['⒡'])  ### PARENTHESIZED LATIN SMALL LETTER F
  create_key_or_plusEquals_to_its_value(triples, "(g)", ['⒢'])  ### PARENTHESIZED LATIN SMALL LETTER G
  create_key_or_plusEquals_to_its_value(triples, "(h)", ['⒣'])  ### PARENTHESIZED LATIN SMALL LETTER H
  create_key_or_plusEquals_to_its_value(triples, "(i)", ['⒤'])  ### PARENTHESIZED LATIN SMALL LETTER I
  create_key_or_plusEquals_to_its_value(triples, "(j)", ['⒥'])  ### PARENTHESIZED LATIN SMALL LETTER J
  create_key_or_plusEquals_to_its_value(triples, "(k)", ['⒦'])  ### PARENTHESIZED LATIN SMALL LETTER K
  create_key_or_plusEquals_to_its_value(triples, "(l)", ['⒧'])  ### PARENTHESIZED LATIN SMALL LETTER L
  create_key_or_plusEquals_to_its_value(triples, "(m)", ['⒨'])  ### PARENTHESIZED LATIN SMALL LETTER M
  create_key_or_plusEquals_to_its_value(triples, "(n)", ['⒩'])  ### PARENTHESIZED LATIN SMALL LETTER N
  create_key_or_plusEquals_to_its_value(triples, "(o)", ['⒪'])  ### PARENTHESIZED LATIN SMALL LETTER O
  create_key_or_plusEquals_to_its_value(triples, "(p)", ['⒫'])  ### PARENTHESIZED LATIN SMALL LETTER P
  create_key_or_plusEquals_to_its_value(triples, "(q)", ['⒬'])  ### PARENTHESIZED LATIN SMALL LETTER Q
  create_key_or_plusEquals_to_its_value(triples, "(r)", ['⒭'])  ### PARENTHESIZED LATIN SMALL LETTER R
  create_key_or_plusEquals_to_its_value(triples, "(s)", ['⒮'])  ### PARENTHESIZED LATIN SMALL LETTER S
  create_key_or_plusEquals_to_its_value(triples, "(t)", ['⒯'])  ### PARENTHESIZED LATIN SMALL LETTER T
  create_key_or_plusEquals_to_its_value(triples, "(u)", ['⒰'])  ### PARENTHESIZED LATIN SMALL LETTER U
  create_key_or_plusEquals_to_its_value(triples, "(v)", ['⒱'])  ### PARENTHESIZED LATIN SMALL LETTER V
  create_key_or_plusEquals_to_its_value(triples, "(w)", ['⒲'])  ### PARENTHESIZED LATIN SMALL LETTER W
  create_key_or_plusEquals_to_its_value(triples, "(x)", ['⒳'])  ### PARENTHESIZED LATIN SMALL LETTER X
  create_key_or_plusEquals_to_its_value(triples, "(y)", ['⒴'])  ### PARENTHESIZED LATIN SMALL LETTER Y
  create_key_or_plusEquals_to_its_value(triples, "(z)", ['⒵'])  ### PARENTHESIZED LATIN SMALL LETTER Z

  create_key_or_plusEquals_to_its_value(triples, "(1)", ['⑴'])  ### PARENTHESIZED DIGIT ONE
  create_key_or_plusEquals_to_its_value(triples, "(2)", ['⑵'])  ### PARENTHESIZED DIGIT TWO
  create_key_or_plusEquals_to_its_value(triples, "(3)", ['⑶'])  ### PARENTHESIZED DIGIT THREE
  create_key_or_plusEquals_to_its_value(triples, "(4)", ['⑷'])  ### PARENTHESIZED DIGIT FOUR
  create_key_or_plusEquals_to_its_value(triples, "(5)", ['⑸'])  ### PARENTHESIZED DIGIT FIVE
  create_key_or_plusEquals_to_its_value(triples, "(6)", ['⑹'])  ### PARENTHESIZED DIGIT SIX
  create_key_or_plusEquals_to_its_value(triples, "(7)", ['⑺'])  ### PARENTHESIZED DIGIT SEVEN
  create_key_or_plusEquals_to_its_value(triples, "(8)", ['⑻'])  ### PARENTHESIZED DIGIT EIGHT
  create_key_or_plusEquals_to_its_value(triples, "(9)", ['⑼'])  ### PARENTHESIZED DIGIT NINE

  create_key_or_plusEquals_to_its_value(  quads, "(10)", ['⑽']) ### PARENTHESIZED NUMBER TEN
  create_key_or_plusEquals_to_its_value(  quads, "(11)", ['⑾']) ### PARENTHESIZED NUMBER ELEVEN
  create_key_or_plusEquals_to_its_value(  quads, "(12)", ['⑿']) ### PARENTHESIZED NUMBER TWELVE
  create_key_or_plusEquals_to_its_value(  quads, "(13)", ['⒀']) ### PARENTHESIZED NUMBER THIRTEEN
  create_key_or_plusEquals_to_its_value(  quads, "(14)", ['⒁']) ### PARENTHESIZED NUMBER FOURTEEN
  create_key_or_plusEquals_to_its_value(  quads, "(15)", ['⒂']) ### PARENTHESIZED NUMBER FIFTEEN
  create_key_or_plusEquals_to_its_value(  quads, "(16)", ['⒃']) ### PARENTHESIZED NUMBER SIXTEEN
  create_key_or_plusEquals_to_its_value(  quads, "(17)", ['⒄']) ### PARENTHESIZED NUMBER SEVENTEEN
  create_key_or_plusEquals_to_its_value(  quads, "(18)", ['⒅']) ### PARENTHESIZED NUMBER EIGHTEEN
  create_key_or_plusEquals_to_its_value(  quads, "(19)", ['⒆']) ### PARENTHESIZED NUMBER NINETEEN
  create_key_or_plusEquals_to_its_value(  quads, "(20)", ['⒇']) ### PARENTHESIZED NUMBER TWENTY

  create_key_or_plusEquals_to_its_value(doubles, "1.", ['⒈'])   ### DIGIT ONE   FULL STOP [for search: DIGIT ONE FULL STOP]
  create_key_or_plusEquals_to_its_value(doubles, "2.", ['⒉'])   ### DIGIT TWO   FULL STOP [for search: DIGIT TWO FULL STOP]
  create_key_or_plusEquals_to_its_value(doubles, "3.", ['⒊'])   ### DIGIT THREE FULL STOP
  create_key_or_plusEquals_to_its_value(doubles, "4.", ['⒋'])   ### DIGIT FOUR  FULL STOP [for search: DIGIT FOUR FULL STOP]
  create_key_or_plusEquals_to_its_value(doubles, "5.", ['⒌'])   ### DIGIT FIVE  FULL STOP [for search: DIGIT FIVE FULL STOP]
  create_key_or_plusEquals_to_its_value(doubles, "6.", ['⒍'])   ### DIGIT SIX   FULL STOP [for search: DIGIT SIX FULL STOP]
  create_key_or_plusEquals_to_its_value(doubles, "7.", ['⒎'])   ### DIGIT SEVEN FULL STOP
  create_key_or_plusEquals_to_its_value(doubles, "8.", ['⒏'])   ### DIGIT EIGHT FULL STOP
  create_key_or_plusEquals_to_its_value(doubles, "9.", ['⒐'])   ### DIGIT NINE  FULL STOP [for search: DIGIT NINE FULL STOP]

  create_key_or_plusEquals_to_its_value(triples, "10.", ['⒑'])  ### NUMBER TEN       FULL STOP [for search: NUMBER TEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "11.", ['⒒'])  ### NUMBER ELEVEN    FULL STOP [for search: NUMBER ELEVEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "12.", ['⒓'])  ### NUMBER TWELVE    FULL STOP [for search: NUMBER TWELVE FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "13.", ['⒔'])  ### NUMBER THIRTEEN  FULL STOP [for search: NUMBER THIRTEEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "14.", ['⒕'])  ### NUMBER FOURTEEN  FULL STOP [for search: NUMBER FOURTEEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "15.", ['⒖'])  ### NUMBER FIFTEEN   FULL STOP [for search: NUMBER FIFTEEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "16.", ['⒗'])  ### NUMBER SIXTEEN   FULL STOP [for search: NUMBER SIXTEEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "17.", ['⒘'])  ### NUMBER SEVENTEEN FULL STOP
  create_key_or_plusEquals_to_its_value(triples, "18.", ['⒙'])  ### NUMBER EIGHTEEN  FULL STOP [for search: NUMBER EIGHTEEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "19.", ['⒚'])  ### NUMBER NINETEEN  FULL STOP [for search: NUMBER NINETEEN FULL STOP]
  create_key_or_plusEquals_to_its_value(triples, "20.", ['⒛'])  ### NUMBER TWENTY    FULL STOP [for search: NUMBER TWENTY FULL STOP]

  create_key_or_plusEquals_to_its_value(triples, "III", ['Ⅲ'])  ###       ROMAN NUMERAL THREE
  create_key_or_plusEquals_to_its_value(triples, "iii", ['ⅲ'])  ### SMALL ROMAN NUMERAL THREE

  create_key_or_plusEquals_to_its_value(triples, "Pts", ['₧'])  ### peseta(s) sign

  create_key_or_plusEquals_to_its_value(triples, "VII", ['Ⅶ'])  ###       ROMAN NUMERAL SEVEN
  create_key_or_plusEquals_to_its_value(triples, "vii", ['ⅶ'])  ### SMALL ROMAN NUMERAL SEVEN

  create_key_or_plusEquals_to_its_value(  quads, "VIII", ['Ⅷ']) ###       ROMAN NUMERAL EIGHT
  create_key_or_plusEquals_to_its_value(  quads, "viii", ['ⅷ']) ### SMALL ROMAN NUMERAL EIGHT

  create_key_or_plusEquals_to_its_value(triples, "XII", ['Ⅻ']) ### ROMAN NUMERAL TWELVE
  create_key_or_plusEquals_to_its_value(triples, "XII", ['Ⅻ']) ### ROMAN NUMERAL TWELVE

  create_key_or_plusEquals_to_its_value(  quads, "a.m.", ['㏂']) ### SQUARE AM
  create_key_or_plusEquals_to_its_value(  quads, "p.m.", ['㏘']) ### SQUARE PM

  create_key_or_plusEquals_to_its_value(  quads, "K.K.", ['㏍']) ### SQUARE KK

  create_key_or_plusEquals_to_its_value(doubles, "AA", ['Ꜳ'])   ### LATIN CAPITAL LETTER AA
# create_key_or_plusEquals_to_its_value(doubles, "AO", ['Ꜵ'])   ### LATIN CAPITAL LETTER AO [disabled b/c its appearance sucks too badly in iTerm2 on MOSX 10.11.6]
# create_key_or_plusEquals_to_its_value(doubles, "ao", ['ꜵ'])   ### LATIN SMALL   LETTER AO [for search: LATIN SMALL LETTER AO] [disabled b/c its appearance sucks too badly in iTerm2 on MOSX 10.11.6]
  create_key_or_plusEquals_to_its_value(doubles, "aa", ['ꜳ'])   ### LATIN SMALL   LETTER AA [for search: LATIN SMALL LETTER AA]

  create_key_or_plusEquals_to_its_value(singles, 'M', 'ꓟ')  ### LISU LETTER MA [this one came out all funky —— wide and overflowing to the right —— in iTerm2 on MOSX 10.11.6 on my main MBP]
  create_key_or_plusEquals_to_its_value(singles, 'N', 'ꓠ')  ### LISU LETTER NA [this one came out all funky —— wide and overflowing to the right —— in iTerm2 on MOSX 10.11.6 on my main MBP]
  create_key_or_plusEquals_to_its_value(singles, 'W', 'ꓪ')  ### LISU LETTER WA [this one came out all funky —— wide and overflowing to the right —— in iTerm2 on MOSX 10.11.6 on my main MBP]
 ### test: 'ꓲ' ### this one is _really_ shit — I can`t seem to get a serif version of this lame-ass fake capital letter I [“LISU LETTER I”]

# create_key_or_plusEquals_to_its_value(doubles, "__", ['_'])  ###
# create_key_or_plusEquals_to_its_value(triples, "___", ['_'])  ###
# create_key_or_plusEquals_to_its_value(  quads, "____", ['_'])  ###



### validate data structures

if DEBUG>9:
  print ("singles:", singles)
for key in singles:
  val = singles[key]
  assert type(val) == type("")
  assert len(val) > 0

for key in doubles:
  ### just require some kind of “iterable”, i.e. don`t _insist_ on a _list_ of strings [even though that`s what is expected]
  val = doubles[key]
  assert len(val) > 0
  for supposed_string in val:
    assert type(supposed_string) == type("")
    assert len( supposed_string) > 0

for key in triples:
  ### just require some kind of “iterable”, i.e. don`t _insist_ on a _list_ of strings [even though that`s what is expected]
  val = triples[key]
  assert len(val) > 0
  for supposed_string in val:
    assert type(supposed_string) == type("")
    assert len( supposed_string) > 0

if DEBUG>9:
  print ("quads:", quads)
for key in   quads:
  ### just require some kind of “iterable”, i.e. don`t _insist_ on a _list_ of strings [even though that`s what is expected]
  val =   quads[key]
  assert len(val) > 0
  for supposed_string in val:
    assert type(supposed_string) == type("")
    assert len( supposed_string) > 0



def output_all_variations_of(prefix, body): ### the input better be at least string-𝒍𝒊𝒌𝒆, or expect all hell to break loose
  assert len(body) >= 0

  if (len(body)>3) and (body[:4] in quads):
    for head in quads[body[:4]]:
      output_all_variations_of(prefix + head, body[4:])

  if (len(body)>2) and (body[:3] in triples):
    for head in triples[body[:3]]:
      output_all_variations_of(prefix + head, body[3:])

  if (len(body)>1) and (body[:2] in doubles):
    for head in singles[body[:2]]:
      output_all_variations_of(prefix + head, body[2:])

  if 1 == len(body):
    if (body[0] in singles):
      for head in singles[body[0]]:
        print (prefix + head)
    else: ### can`t replace/translate it at all, so just output the first char. verbatim
        print (prefix + body)
  elif len(body) > 0:
    if (body[0] in singles):
      for head in singles[body[0]]:
        output_all_variations_of(prefix + head, body[1:])
    else: ### can`t replace/translate it at all, so just output the first char. verbatim
      output_all_variations_of(prefix + body[0], body[1:])



if type(args.output_all_variations_of) == type(""):
  if len(args.output_all_variations_of) < 1:
    print ("ERROR: empty input to “output_all_variations_of”.", file = sys.stderr)
    sys.exit(-1)

  output_all_variations_of("", args.output_all_variations_of)

  sys.exit(0)



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
