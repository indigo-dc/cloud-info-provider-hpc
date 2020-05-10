# cloud-info-provider-hpc

Python scripts for generating info about computing resources from SLURM and QCG.

The description is printed to standard output in JSON format and can be sent as a service to CMDB using scripts from https://github.com/indigo-dc/bulksend2cmdb4hpc. 


## cloud-info-provider-slurm

Gets the info about resources (partitions and nodes) from SLURM.
The resources are get using sinfo command.

The script has no CLI parameters. It reads the header from standard input, where one can put additional static info not available from SLURM.
The header is added at the beginning of service description and should be in JSON format without { and } braces.
The "examples" directory contains shell scripts and header data with example of use.

__Note: the cloud-info-provider-slurm requires access to the Slurm deployment. The central implementation of cloud-info-provider uses a remote API where this data is available__


## cloud-info-provider-qcg

Gets the info about resources (queues and nodes) from QCG.
The resources are get with HTTP request to QCG api.

The script has following CLI parameters:
*  **--qcg-url**       URL of the QCG endpoint
*  **--token**         OIDC token
*  **--verbose**       Verbose output
*  **--debug**         Debug output

It reads the header from standard input, where one can put additional static info not available from QCG.
The header is added at the beginning of service description and should be in JSON format without { and } braces.
The "examples" directory contains shell scripts and header data with example of use.
