import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TH1F, TLatex
sys.argv = tmpargv
import math as m

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

histos = []
histos.append(infile.Get("myana/myana_ecaltrig_01GeV"))
histos.append(infile.Get("myana/myana_ecaltrig_15GeV"))
histos.append(infile.Get("myana/myana_ecaltrig_20GeV"))
histos.append(infile.Get("myana/myana_ecaltrig_25GeV"))
histos.append(infile.Get("myana/myana_ecaltrig_30GeV"))
nevents = histo.GetEntries()

energies = [100., 1500., 2000., 2500., 3000.]
labels = ["> 0.1 GeV", "> 1.5 GeV", "> 2.0 GeV", "> 2.5 GeV", "> 3.0 GeV"]
total_events = histos[0].GetBinContent(1)
beam_rate = 37.e6 #Hz
time = total_events / beam_rate
print(time)

openPDF(outfile,c)

color = 1
for i in range(len(histos)):
    histos[i].Sumw2()
    histos[i].Scale(1 / time / 1000.)
    if (i == 0):
        histos[i].SetTitle("Trigger Rate for Esum > E and zmin > z")
        histos[i].GetXaxis().SetTitle("z [mm]")
        histos[i].GetYaxis().SetTitle("Rate at zmin > z [kHz]")
        histos[i].GetYaxis().SetRangeUser(1.e-3,1e5)
        histos[i].SetLineColor(color)
        histos[i].Draw()
        legend = TLegend(.58,.66,.92,.87)
        legend.SetBorderSize(0)
        legend.SetFillColor(0)
        legend.SetFillStyle(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.035)
        legend.AddEntry(histos[i],labels[i],"LP")
        color = color + 1
        if(color == 5): color = color + 1
    histos[i].SetLineColor(color)
    histos[i].Draw("same")
    legend.AddEntry(histos[i],labels[i],"LP")
legend.Draw()

c.SetLogy(1)
c.Print(outfile+".pdf")
closePDF(outfile,c)
