#!/usr/bin/env python3
from os import urandom

random = urandom(64)

open('keys', 'a+').close()

with open('keys', 'r+') as f:
    text = f.read()
    if len(text.strip()) and not text.endswith('\n'):
        f.write('\n')
    f.write(random.hex() + '\n')
