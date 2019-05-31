#!/usr/bin/env python

import argparse
import logging
import sys
import requests

def parse_opts():
    """
        Parse CLI arguments
    """
    parser = argparse.ArgumentParser(
        description='Get QCG resorces',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@',
        conflict_handler="resolve",
    )
    parser.add_argument(
        '--qcg-url',
        required=True,
        help=('URL of the QCG endpoint'))
    parser.add_argument(
        '--token',
        required=True,
        help=('OIDC token'))
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help=('Verbose output'))
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help=('Debug output'))
    return parser.parse_args()

def set_logging(opts):
    """
        Set logging levels
    """
    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('requests').setLevel(logging.DEBUG)
        logging.getLogger('urllib3').setLevel(logging.DEBUG)
    elif opts.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

def get_header():
    """
        Get header from standard input
    """
    header = ''
    for line in sys.stdin.readlines():
        header += line.strip().rstrip('\n')
    return header

def get_resources(opts):
    """
        Get QCG resources
    """
    url = opts.qcg_url + '/resources/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer %s" % opts.token
    }
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.text
    logging.error("Unable to get resources: %s" % r.status_code)
    logging.error("Response %s" % r.text)
    sys.exit(1)

def format_qcg_info(header, resources):
    return '{' + header + resources[1:]

def main():
    """
        Get info about QCG resources
    """
    opts = parse_opts()
    set_logging(opts)
    header = get_header()
    resources = get_resources(opts)
    json = format_qcg_info(header, resources)
    print json

if __name__ == '__main__':
    main()
