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

histo = infile.Get("myana/myana_trigNLayMuonPair")
histo.Sumw2()
#nevents = histo.GetEntries()
nevents = infile.Get("myana/myana_mupair").GetBinContent(2)

histo2 = infile.Get("myana/myana_nHitsMaxMuonPair")
histo2.Sumw2()

h = TH1F("h", "h", histo.GetNbinsX(), histo.GetXaxis().GetBinLowEdge(1), histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX()))
h2 = TH1F("h2", "h2", histo2.GetNbinsX(), histo2.GetXaxis().GetBinLowEdge(1), histo2.GetXaxis().GetBinUpEdge(histo2.GetNbinsX()))

for i in range(1, h.GetNbinsX()):
    n = histo.Integral(i,histo.GetNbinsX())
    ineff = 1 - n / float(nevents)
    h.SetBinContent(i, ineff)
    error = np.sqrt(nevents - n)/nevents
    h.SetBinError(i, error)

for i in range(1, h2.GetNbinsX()):
    n = histo2.Integral(i,histo2.GetNbinsX())
    ineff = 1 - n / float(nevents)
    h2.SetBinContent(i, ineff)
    error = np.sqrt(nevents - n)/nevents
    h2.SetBinError(i, error)

openPDF(outfile,c)
h.Draw()
h.SetTitle("Trigger Inefficiency Gamma -> Mu+Mu- Sample {0}".format(label))
h.GetXaxis().SetTitle("Blocks Required")
h.GetYaxis().SetTitle("Inefficiency")
c.SetLogy(1)
c.Print(outfile+".pdf")

histo.Draw()
histo.SetTitle("Maximum Consec. Blocks within PE Range: Gamma -> Mu+Mu- Sample {0}".format(label))
histo.GetXaxis().SetTitle("Max Consec. Blocks")
histo.GetYaxis().SetTitle("Events (A.U.)")
c.SetLogy(1)
c.Print(outfile+".pdf")

histo2.Draw()
histo2.SetTitle("Maximum Hits on MIP Track Gamma -> Mu+Mu- Sample  {0}".format(label))
histo2.GetXaxis().SetTitle("Maximum Hits on Track")
histo2.GetYaxis().SetTitle("Events (A.U.)")
c.SetLogy(1)
c.Print(outfile+".pdf")

h2.Draw()
h2.SetTitle("Tracking Inefficiency Gamma -> Mu+Mu- Sample {0}".format(label))
h2.GetXaxis().SetTitle("Layers Required")
h2.GetYaxis().SetTitle("Inefficiency")
c.SetLogy(1)
c.Print(outfile+".pdf")

closePDF(outfile,c)
