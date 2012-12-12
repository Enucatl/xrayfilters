#!/usr/bin/env python
from __future__ import division, print_function
import ROOT
from transmission import Transmission, Spectrum

ROOT.gROOT.ProcessLine(".L update_histogram.C+")

lead = Transmission(82, 0.1)
spectrum = Spectrum("spekcalc_end100.dat")

ROOT.update_histogram(lead.graph, lead.histogram, 0.2, 10, 200)
