import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erf

def single_chan(nsig):
    single_chan_prob = (1 - erf(nsig / np.sqrt(2))) * 0.5
    return single_chan_prob

def prob(nsig, nchan):
    single_chan_prob = single_chan(nsig)
    probability = 1. - ((1. - single_chan_prob)**nchan)
    return probability

def prob_sum(nsig, nchan):
    single_chan_prob = single_chan(nsig * np.sqrt(2))
    #single_chan_prob = single_chan(nsig)
    probability = 1. - ((1. - single_chan_prob)**(nchan/2))
    return probability

def prob_pair(nsig, nchan):
    single_chan_prob = single_chan(nsig)
    double_chan_prob = single_chan_prob**2
    probability = 1. - ((1. - double_chan_prob)**(nchan/2))
    return probability

def prob_asym(nsig, nsig2, nchan):
    single_chan_prob = single_chan(nsig)
    single_chan_prob2 = single_chan(nsig2)
    double_chan_prob = single_chan_prob * single_chan_prob2
    probability = 1. - ((1. - double_chan_prob)**(nchan/2))
    return probability

chan = 100*2*4*10
fig1, ax1 = plt.subplots(1, 1)

sig = np.linspace(0, 7, 71)
sig = np.linspace(0, 7, 700)
single_probs = []
pair_probs = []
sum_probs = []
pair_probs_1 = []
pair_probs_2 = []
pair_probs_3 = []
probs = []
for i in range(len(sig)):
    #if (i%10 == 0):
        #print("{0}  {1}  {2} {3}".format(sig[i], prob(sig[i], chan), single_chan(sig[i]), prob_pair(sig[i], chan)))
    single_probs.append(single_chan(sig[i]))
    pair_probs.append(prob_pair(sig[i], chan))
    sum_probs.append(prob_sum(sig[i], chan))
    pair_probs_1.append(prob_asym(sig[i], 1., chan))
    pair_probs_2.append(prob_asym(sig[i], 2., chan))
    pair_probs_3.append(prob_asym(sig[i], 3., chan))
    probs.append(prob(sig[i], chan))

ax1.scatter(sig, probs, label = "Single Channel", marker='.', linestyle='-')
ax1.scatter(sig, pair_probs, label = "Double Channel", marker='.', linestyle='-')
ax1.scatter(sig, sum_probs, label = "Channel Average", marker='.', linestyle='-')
#ax1.scatter(sig, single_probs, label = "Only One")
ax1.set_title("Event Veto Fraction - Double Channel Requirements")
ax1.set_xlabel("N Sigma")
ax1.set_ylabel("Event Veto Fraction")
ax1.set_xlim(0,6)
ax1.set_ylim(1e-4,1)
ax1.set_yscale('log')
ax1.legend()
plt.grid()

fig2, ax2 = plt.subplots(1, 1)

ax2.scatter(sig, probs, label = "Single Channel", marker='.', linestyle='-')
ax2.scatter(sig, pair_probs_1, label = "Double Channel; Sigma = 1", marker='.', linestyle='-')
ax2.scatter(sig, pair_probs_2, label = "Double Channel; Sigma = 2", marker='.', linestyle='-')
ax2.scatter(sig, pair_probs_3, label = "Double Channel; Sigma = 3", marker='.', linestyle='-')
ax2.set_title("Event Veto Fraction - Asymmetric Requirement")
ax2.set_xlabel("N Sigma")
ax2.set_ylabel("Event Veto Fraction")
ax2.set_xlim(0,6)
ax2.set_ylim(1e-4,1)
ax2.set_yscale('log')
ax2.legend()
plt.grid()

fig3, ax3 = plt.subplots(1, 1)
ax3.scatter(sig, probs, label = "Single Channel", marker='.', linestyle='-')
ax3.set_title("Event Veto Fraction - Single Channel Requirement")
ax3.set_xlabel("N Sigma")
ax3.set_ylabel("Event Veto Fraction")
ax3.set_xlim(0,6)
ax3.set_ylim(1e-4,1)
ax3.set_yscale('log')
ax3.legend()
plt.grid()

plt.show()
