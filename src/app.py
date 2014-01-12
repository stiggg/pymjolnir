__author__ = 'stig'

import envoy
import re
import numpy as np

def calc_result(concurrencies):
    means = []
    stds = []

    for concurrency in concurrencies:
        requests = concurrency * 100

        filename = 'ab-test-{}-{}.txt'.format(str(concurrency), requests)

        print 'running benchmark with concurrency {}, total requests {}...\n'.format(str(concurrency), requests)

        response = envoy.run('ab -c {} -n {} {}'.format(str(concurrency), requests, url))

#        print response.std_err

        match = regex.search(response.std_out)

        means.append(float(match.group('mean')))
        stds.append(float(match.group('std')))

    return means, stds

def format_result(result, means, stds):
    result = np.append(result, [means], axis=0)
    result = np.append(result, [stds], axis=0)

    return result

def save_result(result):
    np.savetxt('test3.out', np.transpose(result), delimiter=',', fmt='%1.2f')

url = 'http://13in12.com/'

#concurrencies = [8, 16, 32, 64, 128, 256]
concurrencies = [1, 2]

# min, mean, std, median, max for processing times
regex = re.compile('Processing:\s*(?P<min>[0-9\.]*)\s*(?P<mean>[0-9\.]*)\s*(?P<std>[0-9\.]*)\s*(?P<median>[0-9\.]*)\s*(?P<max>[0-9\.]*)')

result = np.array([concurrencies])

means, stds = calc_result(concurrencies)
result = format_result(result, means, stds)
save_result(result)
