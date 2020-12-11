#!/usr/local/bin/python2.7

# 
# Submit Batch Job general script
#
#       author: Matt Solt
#

import argparse
import sys
import subprocess
import time

def main() : 

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputFile",   help="Output File.")
    parser.add_argument("-n", "--nFiles",   help="Number of Files to produce.")
    parser.add_argument("-c", "--script",   help="Input script.")
    parser.add_argument("-W", "--time",   help="Time of job for batch.")
    parser.add_argument("-l", "--log",   help="Log file")

    args = parser.parse_args()

    if args.script is None : 
        print ("A input script needs to be specified.") 
        sys.exit(2)

    #Time of each batch job. Default is no batch job submitted
    bsub = ""
    if(args.time is not None):
        bsub = "bsub -W " + args.time

    for i in range(args.nFiles): 
        outfile = "{0}_{1}.root".format(args.outputFile, i)
        print ("Processing file: {0}".format(outfile))
        command = "{0} -o {1} fire {2} {3} {4}".format(bsub, args.log, args.script, i, outfile)
        subprocess.Popen(command, shell=True).wait() 
        time.sleep(0.1)

if __name__ == "__main__" : 
    main() 

