#!/usr/bin/env python3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.argv = ['main.py', '-t', '开发一个电商网站']

from main import main

with open('demo_output.txt', 'w', encoding='utf-8') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    try:
        main()
    finally:
        sys.stdout = old_stdout