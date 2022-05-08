#!/usr/bin/env python3

import argparse
from random import randrange

parser = argparse.ArgumentParser()
parser.add_argument("--num_lines", required=True, type=int)
args = parser.parse_args()

assert type(args.num_lines) == type(9)


### hard-coded, for now
NUM_CHARS_PER_LINE=79

for line_num in range(args.num_lines):
  print ( "".join([chr( randrange(32, 127) ) for _ in range(NUM_CHARS_PER_LINE)]) )
