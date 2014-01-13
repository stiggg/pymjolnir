__author__ = 'stig'

import argparse
import sys
import numpy as np
from pymjolnir.mjolnir import Mjolnir

def command_line_parse(default_concurrencies):
    parser = argparse.ArgumentParser(description='Website load tester: Wraps ab to load test website '
                                                 'with different number of concurrent users.')
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='output file')
    parser.add_argument('-c', '--concurrencies', nargs='*', type=int,
                        default=default_concurrencies, help='list of concurrent requests, i.e. "8 16 32"')
    parser.add_argument('url', help='url to load test')

    args = parser.parse_args()

    return args

def save_result(result, output_file):
    np.savetxt(output_file, result, delimiter=',', fmt='%1.2f')

def main():
    default_concurrencies = [8, 16, 32, 64, 128, 256]

    args = command_line_parse(default_concurrencies)

    hammer = Mjolnir()
    result = hammer.strike(args.url, args.concurrencies)

    save_result(result, args.output)

if __name__ == "__main__":
    main()