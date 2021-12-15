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

histo = infile.Get("myana/myana_ecalenergysum_ecalz")
nevents = histo.GetEntries()

histos = []
energies = [100., 1500., 2000., 2500., 3000.]
labels = ["> 0.1 GeV", "> 1.5 GeV", "> 2.0 GeV", "> 2.5 GeV", "> 3.0 GeV"]
n_z = 100
minz =200.
maxz = 800.
total_events = histo.GetEntries()
beam_rate = 37.e6 #Hz
time = total_events / beam_rate
print(time)

for i in range(len(energies)):
    energy = energies[i]
    histo_e = TH1F(labels[i], labels[i], n_z, minz, maxz)
    for j in range(n_z):
        z = minz + j * (maxz - minz) / (n_z - 1)
        n_events = 0
        for k in range(1, histo.GetNbinsX()):
          for l in range(1, histo.GetNbinsY()):
            if(histo.GetXaxis().GetBinLowEdge(k) <= z and histo.GetXaxis().GetBinUpEdge(k) >= z and histo.GetYaxis().GetBinLowEdge(l) >= energy):
              n_events = n_events + histo.GetBinContent(k, l)
        histo_e.SetBinContent(j+1, n_events / time / 1000.)
        histo_e.SetBinError(j+1, m.sqrt(n_events) / time / 1000.)
    histos.append(histo_e)
    del histo_e

openPDF(outfile,c)
histos[0].SetTitle("Trigger Rate for Esum > E and zmin > z")
histos[0].GetXaxis().SetTitle("z [mm]")
histos[0].GetYaxis().SetTitle("Rate at zmin > z [kHz]")
histos[0].GetYaxis().SetRangeUser(1.e-3,1e5)
histos[0].SetLineColor(1)
histos[0].Draw()
legend = TLegend(.58,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(histos[0],labels[0],"LP")
color = 1
for i in range(1, len(histos)):
    color = color + 1
    if(color == 5): color = color + 1
    histos[i].SetLineColor(color)
    histos[i].Draw("same")
    legend.AddEntry(histos[i],labels[i],"LP")
legend.Draw()

c.SetLogy(1)
c.Print(outfile+".pdf")
closePDF(outfile,c)
