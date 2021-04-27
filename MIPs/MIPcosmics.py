#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 15:59:09 2020

@author: matthewsolt
"""

import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import numpy as np
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
    print ("\nUsage: {0} <output file base name> <input file>".format(sys.argv[0]))
    print ('\t-l: plot label')
    print ('\t-h: this help message')
    print

label = ""

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hl:')

# Parse the command line arguments
for opt, arg in options:
    if opt=='-l':
        label = str(arg)
    if opt=='-h':
        print_usage()
        sys.exit(0)

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

infile = TFile(remainder[1])

histo = infile.Get("myana/myana_trigNLay")
nevents = histo.Integral(2,75)
print(nevents)

#h = TH1F("h", "h", histo.GetNbinsX(), histo.GetXaxis().GetBinLowEdge(1), histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX()))
h = TH1F("h", "h", 75, 0, 75)

cosmicrate = 4.58 #kHz
time = nevents / (cosmicrate * 1000) # seconds

for i in range(2, h.GetNbinsX()):
    n = histo.Integral(i,histo.GetNbinsX())
    rate = n / time * 0.001 #kHz
    h.SetBinContent(i, rate)
    error = 0
    if(n != 0):
        error = np.sqrt(1/n) * rate
    else:
        error = np.sqrt(1/2.) * rate
    h.SetBinError(i, error)

histo2 = infile.Get("myana/myana_nHitsMax")
histo2.Sumw2()
#histo2.Scale(1/nevents)
#h3 = TH1F("h3", "h3", 20, 0, 20)
#for i in range(h3.GetNbinsX()):
    #h3.SetBinContent(i, histo2.GetBinContent(i))
    #h3.SetBinError(i, histo2.GetBinError(i))

openPDF(outfile,c)
h.Draw()
h.SetTitle("Trigger Rate Cosmic Sample {0}".format(label))
h.GetXaxis().SetTitle("Min Blocks Required")
h.GetYaxis().SetTitle("Trigger Rate kHz")
c.SetLogy(1)
c.Print(outfile+".pdf")

histo.Sumw2()
histo.Scale(0.001/time)
#h2 = TH1F("h2", "h2", 20, 0, 20)
#for i in range(h2.GetNbinsX()):
    #h2.SetBinContent(i, histo.GetBinContent(i))
    #h2.SetBinError(i, histo.GetBinError(i))

histo.Draw()
histo.SetTitle("Maximum Consec. Blocks within PE Range: Cosmic Sample  {0}".format(label))
histo.GetXaxis().SetTitle("Max Consec. Blocks")
histo.GetYaxis().SetTitle("Rate (kHz)")
c.SetLogy(1)
c.Print(outfile+".pdf")

histo2.Draw()
histo2.SetTitle("Maximum Hits on MIP Track Cosmic Sample  {0}".format(label))
histo2.GetXaxis().SetTitle("Maximum Hits on Track")
histo2.GetYaxis().SetTitle("Events (A.U.)")
c.SetLogy(1)
c.Print(outfile+".pdf")

closePDF(outfile,c)
