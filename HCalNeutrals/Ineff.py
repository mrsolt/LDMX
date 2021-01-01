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
    print ('\t-h: this help message')
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
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
infile2 = TFile(remainder[2])
infile3 = TFile(remainder[3])

histo = infile.Get("myana/myana_lambda_max")
nevents = histo.GetEntries()

histo2 = infile2.Get("myana/myana_lambda_max")
nevents2 = histo2.GetEntries()

histo3 = infile3.Get("myana/myana_lambda_max")
nevents3 = histo3.GetEntries()

h = TH1F("h", "h", histo.GetNbinsX(), histo.GetXaxis().GetBinLowEdge(1), histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX()))
h2 = TH1F("h2", "h2", histo2.GetNbinsX(), histo2.GetXaxis().GetBinLowEdge(1), histo2.GetXaxis().GetBinUpEdge(histo2.GetNbinsX()))
h3 = TH1F("h3", "h3", histo3.GetNbinsX(), histo3.GetXaxis().GetBinLowEdge(1), histo3.GetXaxis().GetBinUpEdge(histo3.GetNbinsX()))

for i in range(h.GetNbinsX()):
    n = histo.Integral(1,i)
    ineff = 1 - n / float(nevents)
    h.SetBinContent(i, ineff)
    
for i in range(h2.GetNbinsX()):
    n = histo2.Integral(1,i)
    ineff = 1 - n / float(nevents2)
    h2.SetBinContent(i, ineff)
    
for i in range(h3.GetNbinsX()):
    n = histo3.Integral(1,i)
    ineff = 1 - n / float(nevents3)
    h3.SetBinContent(i, ineff)
    
#histo2 = infile.Get("myana/myana_lambda_max")
#nevents2 = histo2.GetEntries()

#h2 = TH1F("h2", "h2", histo2.GetNbinsX(), histo2.GetXaxis().GetBinLowEdge(1), histo2.GetXaxis().GetBinUpEdge(histo2.GetNbinsX()))
#for i in range(h2.GetNbinsX()):
#    n = histo2.Integral(1,i)
#    ineff = 1 - n / float(nevents2)
#    h2.SetBinContent(i, ineff)
    
openPDF(outfile,c)
h.SetLineColor(1)
h2.SetLineColor(2)
h3.SetLineColor(4)
h.Draw()
h.SetTitle("Inefficiency")
h.GetXaxis().SetTitle("#lambda")
h.GetYaxis().SetTitle("Inefficiency")
h2.Draw("same")
h3.Draw("same")
legend = TLegend(.58,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(h,"10.2","LP")
legend.AddEntry(h2,"10.3","LP")
legend.AddEntry(h3,"10.5","LP")
legend.Draw()
c.SetLogy(1)
c.Print(outfile+".pdf")

#h2.Draw()
#h2.SetTitle("Inefficiency")
#h2.GetXaxis().SetTitle("#lambda")
#h2.GetYaxis().SetTitle("Inefficiency")
#c.Print(outfile+".pdf")
closePDF(outfile,c)
