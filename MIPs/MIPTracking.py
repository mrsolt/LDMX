import sys
tmpargv = sys.argv
sys.argv = []
import getopt
import ROOT
from ROOT import gROOT, TFile, TTree, TChain, gDirectory, TLine, gStyle, TCanvas, TLegend, TLatex
sys.argv = tmpargv

#List arguments
def print_usage():
    print "\nUsage: {0} <output file base name> <input file name>".format(sys.argv[0])
    print "Arguments: "
    print '\t-h: this help message'
    print

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h')

# Parse the command line arguments
for opt, arg in options:
        if opt=='-h':
            print_usage()
            sys.exit(0)

gStyle.SetOptStat(0)
c = TCanvas("c","c",800,600)

outfile = remainder[0]
infile = TFile(remainder[1])

def openPDF(outfile,canvas):
	canvas.Print(outfile+".pdf[")

def closePDF(outfile,canvas):
	canvas.Print(outfile+".pdf]")

def getHisto(histoTitle,infile):
	histo = infile.Get(histoTitle)
	return histo

def fitHisto(histo, canvas, XaxisTitle="",YaxisTitle="",plotTitle="",stats=1):
    histo.Sumw2()
    histo.Scale(1./100000)
    histo.Draw("")
    histo.SetTitle(plotTitle)
    histo.GetXaxis().SetTitle(XaxisTitle)
    histo.GetYaxis().SetTitle(YaxisTitle)
    histo.SetStats(stats)
    histo.Fit("gaus")
    canvas.Print(outfile+".pdf")

def drawHisto(histo, canvas, XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
    histo.Sumw2()
    histo.Scale(1./100000)
    histo.Draw("COLZ")
    histo.SetTitle(plotTitle)
    histo.GetXaxis().SetTitle(XaxisTitle)
    histo.GetYaxis().SetTitle(YaxisTitle)
    histo.SetStats(stats)
    canvas.Print(outfile+".pdf")

def drawHisto2(histo, histo2, legend, canvas, XaxisTitle="",YaxisTitle="",plotTitle="",stats=0):
    histo.Sumw2()
    histo.Scale(1./100000 *0.12)
    histo2.Sumw2()
    histo2.Scale(1./100000)
    maximum = histo.GetMaximum()
    if(histo2.GetMaximum() > maximum):
        maximum = histo2.GetMaximum()
    histo.GetYaxis().SetRangeUser(0, 1.2 * maximum)
    histo.Draw("")
    histo2.SetLineColor(2)
    histo.SetTitle(plotTitle)
    histo.GetXaxis().SetTitle(XaxisTitle)
    histo.GetYaxis().SetTitle(YaxisTitle)
    histo.SetStats(stats)
    histo2.Draw("same")
    legend.Draw("same")
    canvas.Print(outfile+".pdf")

startx_truth = getHisto("myana/myana_startx", infile)
starty_truth = getHisto("myana/myana_starty", infile)
startx_reco = getHisto("myana/myana_x", infile)
starty_reco = getHisto("myana/myana_y", infile)

startdx_truth = getHisto("myana/myana_startdx", infile)
startdy_truth = getHisto("myana/myana_startdy", infile)
startdx_reco = getHisto("myana/myana_dx", infile)
startdy_reco = getHisto("myana/myana_dy", infile)

legend = TLegend()
legend = TLegend(.68,.66,.92,.87)
legend.SetBorderSize(0)
legend.SetFillColor(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.035)
legend.AddEntry(startx_truth,"truth","LP")
legend.AddEntry(startx_reco,"reco","LP")

openPDF(outfile, c)

drawHisto2(startx_truth, startx_reco, legend, c, XaxisTitle="start x [mm]",YaxisTitle="",plotTitle="Projected X at Front Hcal Face")
drawHisto2(starty_truth, starty_reco, legend, c, XaxisTitle="start y [mm]",YaxisTitle="",plotTitle="Projected Y at Front Hcal Face")
drawHisto2(startdx_truth, startdx_reco, legend, c, XaxisTitle="start dx/dz",YaxisTitle="",plotTitle="Projected dx/dz at Front Hcal Face")
drawHisto2(startdy_truth, startdy_reco, legend, c, XaxisTitle="start dy/dz",YaxisTitle="",plotTitle="Projected dy/dz at Front Hcal Face")

pe = getHisto("myana/myana_PEiso", infile)
c.SetLogy(1)
drawHisto(pe, c, XaxisTitle="PE",YaxisTitle="",plotTitle="Isolated Hit PEs")
c.SetLogy(0)

rechits = getHisto("myana/myana_HcalRecHits", infile)
rechitsMIP = getHisto("myana/myana_HcalRecHitsMIP", infile)
rechitsIso = getHisto("myana/myana_HcalRecHitsIso", infile)
drawHisto(rechits, c, XaxisTitle="Layer",YaxisTitle="Strip",plotTitle="Hcal Reconstructed Hits")
drawHisto(rechitsMIP, c, XaxisTitle="Layer",YaxisTitle="Strip",plotTitle="Hcal Reconstructed Hits Above MIP Threshold")
drawHisto(rechitsIso, c, XaxisTitle="Layer",YaxisTitle="Strip",plotTitle="Hcal Isolated Reconstructed Hits")

pullx = getHisto("myana/myana_pullx", infile)
pully = getHisto("myana/myana_pully", infile)
pulldx = getHisto("myana/myana_pulldx", infile)
pulldy = getHisto("myana/myana_pulldy", infile)
gStyle.SetOptFit(1011);
fitHisto(pullx, c, XaxisTitle="Pull x",YaxisTitle="",plotTitle="Pull x")
fitHisto(pully, c, XaxisTitle="Pull y",YaxisTitle="",plotTitle="Pull y")
fitHisto(pulldx, c, XaxisTitle="Pull dx/dz",YaxisTitle="",plotTitle="Pull dx/dz")
fitHisto(pulldy, c, XaxisTitle="Pull dy/dz",YaxisTitle="",plotTitle="Pull dy/dz")

startlay = getHisto("myana/myana_trackstartlayer", infile)
endlay = getHisto("myana/myana_trackendlayer", infile)
legend2 = TLegend()
legend2 = TLegend(.68,.66,.92,.87)
legend2.SetBorderSize(0)
legend2.SetFillColor(0)
legend2.SetFillStyle(0)
legend2.SetTextFont(42)
legend2.SetTextSize(0.035)
legend2.AddEntry(startlay,"Start","LP")
legend2.AddEntry(endlay,"End","LP")
drawHisto2(startlay, endlay, legend2, c, XaxisTitle="Layer",YaxisTitle="",plotTitle="Track Start/End Layer")

tracks = getHisto("myana/myana_tracks", infile)
nhits = getHisto("myana/myana_nHitsMax", infile)
c.SetLogy(1)
drawHisto(tracks, c, XaxisTitle="Track Multiplicity",YaxisTitle="",plotTitle="Track Multiplicity")
drawHisto(nhits, c, XaxisTitle="Number of Hits",YaxisTitle="",plotTitle="Maximum Number of Hits on Track")

closePDF(outfile, c)
