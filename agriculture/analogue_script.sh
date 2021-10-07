#!/bin/bash

# latitude : $1
# longitude : $2
# refs_array_file : $3

mpiexec -n 8 /opt/Agriculture/agriculture-venv/bin/python3.8 /opt/Agriculture/agriculture/ccaf.py $1 $2 $3