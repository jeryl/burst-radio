#!/usr/bin/env python
import sys
import time



def run():
    while True:
        with open(sys.argv[1], 'r') as f:
            sys.stdout.write(f.read())
            sys.stdout.write('\n.\n')
            sys.stdout.flush()
        time.sleep(5)


if __name__ == '__main__':
    run()
