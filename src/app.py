__author__ = 'stig'

import envoy
import re
import numpy as np
import argparse
import sys

def calc_result(concurrencies, url):
    means = []
    stds = []

    for concurrency in concurrencies:
        #requests = concurrency * 100
        requests = concurrency * 10

        #filename = '/tmp/ab-test-{}-{}.txt'.format(str(concurrency), requests)

        print 'running benchmark with concurrency {}, total requests {}...'.format(str(concurrency), requests)

        response = envoy.run('ab -c {} -n {} {}'.format(str(concurrency), requests, url))

        if response.std_err != '':
            print(response.std_err)
            sys.exit()

        # min, mean, std, median, max for processing times
        regex = re.compile('Processing:\s*(?P<min>[0-9\.]*)\s*(?P<mean>[0-9\.]*)\s*(?P<std>[0-9\.]*)\s*(?P<median>[0-9\.]*)\s*(?P<max>[0-9\.]*)')
        match = regex.search(response.std_out)

        means.append(float(match.group('mean')))
        stds.append(float(match.group('std')))

    return (means, stds)

def format_result(result, means, stds):
    result = np.append(result, [means], axis=0)
    result = np.append(result, [stds], axis=0)

    return result

def save_result(result, output_file):
    np.savetxt(output_file, np.transpose(result), delimiter=',', fmt='%1.2f')

#default_concurrencies = [8, 16, 32, 64, 128, 256]
default_concurrencies = [1, 2]

parser = argparse.ArgumentParser(description='Website load tester: Wraps ab to load test website '
                                             'with different number of concurrent users.')
parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, help='output file')
parser.add_argument('-c', '--concurrencies', nargs='*', type=int,
                    default=default_concurrencies, help='list of concurrent requests, i.e. "8 16 32"')
parser.add_argument('url', help='url to load test')

args = parser.parse_args()

means, stds = calc_result(args.concurrencies, args.url)
result = format_result(np.array([args.concurrencies]), means, stds)
save_result(result, args.output)
