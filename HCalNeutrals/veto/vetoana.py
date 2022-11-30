from LDMX.Framework import ldmxcfg

p=ldmxcfg.Process('myana')

# Create an instance of the TB HCal MIP tracking analyzer.
from LDMX.Analysis import HCalVetoAna
#from LDMX.Analysis import TBMipTracking
vetoana = HCalVetoAna.HCalVetoAna("myana")
#vetoana = TBMipTracking.TBMipTracking("mipana")

# Define the order in which the analyzers will be executed.
p.sequence=[vetoana]

# input the file as an argument on the command line
import sys
p.inputFiles=[sys.argv[2]]

# Specify the output file.  When creating ntuples or saving histograms, the
# output file name is specified by setting the attribute histogramFile.
p.histogramFile=sys.argv[1]
