__author__ = 'stig'

import envoy
import re
import numpy as np
import sys

class Mjolnir():
    REQUEST_MULTIPLIER = 10

    def strike(self, url, concurrencies):
        means = []
        stds = []

        for concurrency in concurrencies:
            requests = concurrency * self.REQUEST_MULTIPLIER

            self.output('running benchmark with concurrency {}, total requests {}...'.format(str(concurrency), requests))

            response = self.run_process('ab -q -c {} -n {} {}'.format(str(concurrency), requests, url))

            means, stds = self.parse_response(response, means, stds)

        result = self.format_result(concurrencies, means, stds)

        return result

    def write_ab_files(self, c, r, path='./'):
        filename = '{}ab-test-{}-{}.txt'.format(path, str(c), r)

    def run_process(self, cmd):
        """
        Runs cli command, checks for strerr.
        """

        response = envoy.run(cmd)

        if response.std_err != '':
            print(response.std_err)
            sys.exit()

        return response

    def parse_response(self, response, means, stds):
        """
        Parses ab response for processing times.
        """

        # min, mean, std, median, max for processing times
        regex = re.compile('Processing:\s*(?P<min>[0-9\.]*)\s*(?P<mean>[0-9\.]*)\s*(?P<std>[0-9\.]*)\s*(?P<median>[0-9\.]*)\s*(?P<max>[0-9\.]*)')
        match = regex.search(response.std_out)

        means.append(float(match.group('mean')))
        stds.append(float(match.group('std')))

        return (means, stds)

    def format_result(self, concurrencies, means, stds):
        """
        Create numpy array with concurrency count, mean and standard deviation statistics.
        """
        result = np.array([concurrencies])
        result = np.append(result, [means], axis=0)
        result = np.append(result, [stds], axis=0)

        return np.transpose(result)

    def output(self, string):
        """
        Output strings.
        """
        print(string)