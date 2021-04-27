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
nevents = histo.GetEntries()

#h = TH1F("h", "h", histo.GetNbinsX(), histo.GetXaxis().GetBinLowEdge(1), histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX()))
h = TH1F("h", "h", 20, 0, 20)

pulse = 37 #MHz
mu = 1. #average electons / bunch


for i in range(2, h.GetNbinsX()):
    n = histo.Integral(i,histo.GetNbinsX())
    rate = n * pulse * mu / 1000 #kHz
    h.SetBinContent(i, rate)
    error = 0
    if(n != 0):
        error = np.sqrt(1/n) * rate
    else:
        error = np.sqrt(1/2.) * pulse * mu / 1000.
    h.SetBinError(i, error)

histo2 = infile.Get("myana/myana_nHitsMax")
histo2.Sumw2()
histo2.Scale(1/nevents)
h3 = TH1F("h3", "h3", 20, 0, 20)
for i in range(h3.GetNbinsX()):
    h3.SetBinContent(i, histo2.GetBinContent(i))
    h3.SetBinError(i, histo2.GetBinError(i))

openPDF(outfile,c)
h.Draw()
h.SetTitle("Trigger Rate Inclusive e- Sample {0}".format(label))
h.GetXaxis().SetTitle("Min Blocks Required")
h.GetYaxis().SetTitle("Trigger Rate kHz")
c.SetLogy(1)
c.Print(outfile+".pdf")

histo.Sumw2()
histo.Scale(pulse/1000.*mu)
h2 = TH1F("h2", "h2", 20, 0, 20)
for i in range(h2.GetNbinsX()):
    h2.SetBinContent(i, histo.GetBinContent(i))
    h2.SetBinError(i, histo.GetBinError(i))

h2.Draw()
h2.SetTitle("Maximum Consec. Blocks within PE Range: Inclusive e- Sample  {0}".format(label))
h2.GetXaxis().SetTitle("Max Consec. Blocks")
h2.GetYaxis().SetTitle("Rate (kHz)")
c.SetLogy(1)
c.Print(outfile+".pdf")

h3.Draw()
h3.SetTitle("Maximum Hits on MIP Track Inclusive e- Sample  {0}".format(label))
h3.GetXaxis().SetTitle("Maximum Hits on Track")
h3.GetYaxis().SetTitle("Events / Beam e-")
c.SetLogy(1)
c.Print(outfile+".pdf")

closePDF(outfile,c)
