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

h = TH1F("h", "h", histo.GetNbinsX(), histo.GetXaxis().GetBinLowEdge(1), histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX()))

pulse = 37 #MHz
mu = 1. #average electons / bunch


for i in range(2, h.GetNbinsX()):
    n = histo.Integral(2,i)
    rate = n * / pulse * mu * 1000 #kHz
    h.SetBinContent(i, rate)
    error = sqrt(1/n) * rate
    h.SetError(i, error)

openPDF(outfile,c)
h.Draw()
h.SetTitle("Trigger Rate Inclusive e- Sample {0}".format(label))
h.GetXaxis().SetTitle("Min Blocks Required")
h.GetYaxis().SetTitle("Trigger Rate kHz")
#c.SetLogy(1)
c.Print(outfile+".pdf")

closePDF(outfile,c)
