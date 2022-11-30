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

#Output File
outfile = remainder[0]
outfileroot = TFile(remainder[0]+".root","RECREATE")

#Input File
infile = TFile(remainder[1])

histo_maxPE = infile.Get("myana/myana_maxPE")
histo_baravg = infile.Get("myana/myana_maxPEbaravg")
nevents = histo_maxPE.GetEntries()

histo_sumPEzoomout = infile.Get("myana/myana_sumPEzoomout")
histo_maxPEzoomout = infile.Get("myana/myana_maxPEzoomout")

histo_maxPE.Sumw2()
histo_baravg.Sumw2()
histo_sumPEzoomout.Sumw2()
histo_maxPEzoomout.Sumw2()

#h = TH1F("h", "h", histo.GetNbinsX()/10, histo.GetXaxis().GetBinLowEdge(1), histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX()))

nPEs = 20
h_maxPE = TH1F("h_maxPE", "h_maxPE", nPEs, 0, nPEs)
h_baravg = TH1F("h_baravg", "h_baravg", nPEs, 0, nPEs)

#Calculate the Inefficieny
for i in range(nPEs):
    n_single = histo_maxPE.Integral(0, i+1)
    ineff_single = n_single/ float(nevents)
    #err_single = np.sqrt(nevents - n_single)/nevents #Need to double check if this is calculated correctly
    err_single = np.sqrt((n_single+1)*(n_single+2)/((nevents+2)*(nevents+3)) - (n_single+1)**2/(nevents+2)**2)
    h_maxPE.SetBinContent(i+1, ineff_single)
    h_maxPE.SetBinError(i+1, err_single)

    n_double = histo_baravg.Integral(0, i+1)
    ineff_double = n_double / float(nevents)
    #err_double = np.sqrt(nevents - n_double)/nevents #Need to double check if this is calculated correctly
    err_double = np.sqrt((n_double+1)*(n_double+2)/((nevents+2)*(nevents+3)) - (n_double+1)**2/(nevents+2)**2)
    h_baravg.SetBinContent(i+1, ineff_double)
    h_baravg.SetBinError(i+1, err_double)

#Draw and Save the Histogram
openPDF(outfile,c)
h_maxPE.GetYaxis().SetRangeUser(1.e-6, 1.)
h_maxPE.Draw()
h_maxPE.SetTitle("Inefficiency For 2 GeV Neutrons {0}".format(label))
h_maxPE.GetXaxis().SetTitle("PE threshold")
h_maxPE.GetYaxis().SetTitle("Inefficiency")
h_baravg.SetLineColor(2)
h_baravg.Draw("same")
legend = TLegend(.58,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(h_maxPE,"Single Channel","LP")
legend.AddEntry(h_baravg,"Channel Average","LP")
legend.Draw()
c.SetLogy(1)
c.Print(outfile+".pdf")

#histo_maxPE.GetYaxis().SetRangeUser(1.e-6, 1.)
histo_maxPE.Draw()
histo_maxPE.SetTitle("Single and Average Max PE Distributions 2 GeV Neutrons".format(label))
histo_maxPE.GetXaxis().SetTitle("PEs")
histo_maxPE.GetYaxis().SetTitle("N Events (A.U.)")
histo_baravg.SetLineColor(2)
histo_baravg.Draw("same")
legend2 = TLegend(.58,.16,.92,.37)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(histo_maxPE,"Single Channel","LP")
legend2.AddEntry(histo_baravg,"Channel Average","LP")
legend2.Draw()
c.SetLogy(1)
c.Print(outfile+".pdf")

histo_sumPEzoomout.Draw()
histo_sumPEzoomout.SetTitle("Detector Sum PE Distributions 2 GeV Neutrons".format(label))
histo_sumPEzoomout.GetXaxis().SetTitle("PEs")
histo_sumPEzoomout.GetYaxis().SetTitle("N Events (A.U.)")
c.SetLogy(1)
c.Print(outfile+".pdf")

histo_maxPEzoomout.Draw()
histo_maxPEzoomout.SetTitle("Single Channel Max PE Distributions 2 GeV Neutrons".format(label))
histo_maxPEzoomout.GetXaxis().SetTitle("PEs")
histo_maxPEzoomout.GetYaxis().SetTitle("N Events (A.U.)")
c.SetLogy(1)
c.Print(outfile+".pdf")

closePDF(outfile,c)
