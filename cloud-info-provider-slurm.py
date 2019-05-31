#!/usr/bin/env python

import subprocess
import logging
import sys

def get_output_from_subprocess(command):
    """
        Get output from external shell command
    """
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.readlines()
    retval = p.wait()
    if retval == 0:
        return output
    else:
        logging.error("Unable to execute external shell command: %s" % command)
        sys.exit(1)

def get_header():
    """
        Get header from standard input
    """
    header = ''
    for line in sys.stdin.readlines():
        header += '  '+line
    return header

def format_partitions(partitions):
    """
        Format slurm partitions to JSON format
    """
    output = '  "partitions": [\n'
    row = 0
    for line in partitions:
        row += 1
        if row > 1:
            output += ',\n'
        output += '    {\n'
        output += get_field(line, 'partition_name', 1, 1)
        output += get_field(line, 'default_time_for_job', 2, 1)
        output += get_field(line, 'maximum_time_for_job', 3, 1)
        output += get_field(line, 'nodes', 4, 0)
        output += '    }'
    output += '\n  ],\n'
    return output

def format_nodes(nodes):
    """
        Format slurm nodes to JSON format
    """
    output = '  "nodes_info": [\n'
    row = 0
    for line in nodes:
        row += 1
        if row > 1:
            output += ',\n'
        output += '    {\n'
        line = line.replace('/', ' ')
        output += get_field(line, 'nodes', 9, 1)
        output += get_field(line, 'number_of_nodes', 1, 1)
        output += get_field(line, 'allocated_nodes', 2, 1)
        output += get_field(line, 'idle_nodes', 3, 1)
        output += get_field(line, 'cpus_per_node', 4, 1)
        output += get_field(line, 'memory_per_node_MB', 5, 1)
        output += get_field(line, 'sockets_per_node', 6, 1)
        output += get_field(line, 'cores_per_socket', 7, 1)
        output += get_field(line, 'threads_per_core', 8, 0)
        output += '    }'
    output += '\n  ]\n'
    return output

def get_field(line, field, index, comma):
    """
        Get index-th field from line
    """
    value = line.split()[index-1]
    output = '      "%s": "%s"' % (field, value)
    if comma==1:
        output += ','
    return output + '\n'

def format_slurm_info(partitions, nodes):
    """
        Format slurm info to JSON format
    """
    return '{\n' + get_header() + format_partitions(partitions) + format_nodes(nodes) + '}'

def main():
    """
        Get info about nodes and partitions from slurm
        and convert it to JSON format
    """
    partitions = get_output_from_subprocess('sinfo -h -o "%30P %.12L %.12l %N"')
    nodes = get_output_from_subprocess('sinfo -h -e -o "%.5D %.11A %.3c %.7m %X %.2Y %Z %N" -S "%N"')
    json = format_slurm_info(partitions, nodes)
    print json

if __name__ == '__main__':
    main()
