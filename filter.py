#!/usr/bin/env python
from __future__ import division, print_function
import random
import string
from rootstyle import tdrstyle
from periodic_table import periodic_table
import os
import ROOT
from transmission import Spectrum, Transmission, DetectorEfficiency

tdrstyle()

class Filter(object):
    """the Filter is made of a Spectrum and one or more Transmission. The
    Spectrum also includes the detector and any fixed filters. """

    def __init__(self, spectrum, tr_dict, energy_window):
        super(Filter, self).__init__()
        max_energy = spectrum.max_energy
        min_energy = spectrum.min_energy
        self.energy_window = energy_window
        self.spectrum = spectrum
        self.tr_dict = tr_dict
        histogram_name = " ".join(tr.histogram.GetName()
                for tr in self.tr_dict.itervalues())
        histogram_name += "".join(str(tr.thickness)
                for tr in self.tr_dict.itervalues())
        histogram_name += ''.join(random.choice(string.letters)
                for i in range(5))
        self.histogram = spectrum.histogram.Clone(histogram_name)
        
    def filter(self, change_thickness_of={}):
        if not self.tr_dict:
            return
        else:
            self.pave = ROOT.TPaveText(0.7, 0.7, 0.95, 0.95, "NDC")
            for key, new_thickness in change_thickness_of.iteritems():
                self.tr_dict[key].thickness = new_thickness
            total_filter = sum(self.tr_dict.values()[1:],
                    self.tr_dict.values()[0])
            histogram_name = " ".join(tr.histogram.GetName()
                    for tr in self.tr_dict.itervalues())
            histogram_name += "".join(str(tr.thickness)
                    for tr in self.tr_dict.itervalues())
            self.histogram = self.spectrum.histogram.Clone(histogram_name)
            self.histogram.Multiply(total_filter.histogram)
            element_thickness = ("{0}, x={1:.4f} #(){{cm}}".format(
                periodic_table[tr.element_Z], tr.thickness)
                for tr in self.tr_dict.itervalues())
            for element in element_thickness:
                self.pave.AddText(element)
            min_energy, max_energy = self.energy_window
            first_bin = min_energy - self.spectrum.min_energy + 1
            last_bin = max_energy - self.spectrum.min_energy + 1
            signal_integral = self.histogram.Integral(first_bin, last_bin)
            overflow = self.histogram.Integral(last_bin + 1, self.histogram.GetNbinsX())
            integral = self.histogram.Integral()
            self.pave.SetFillColor(0)
            self.pave.AddText("total flux {0:.3g}".format(integral))
            self.pave.AddText("{0:.1%} between {1[0]:.0f}-{1[1]:.0f} keV".format(
                signal_integral / integral, self.energy_window))
            self.pave.AddText("{0:.1%} over {1:.0f} keV".format(
                overflow / integral, self.energy_window[1]))
            self.pave.AddText("{0:.1%} efficiency".format(self.efficiency()))

    def purity(self):
        min_energy, max_energy = self.energy_window
        first_bin = min_energy - self.spectrum.min_energy + 1
        last_bin = max_energy - self.spectrum.min_energy + 1
        return self.histogram.Integral(first_bin, last_bin) / self.histogram.Integral()

    def efficiency(self):
        return self.histogram.Integral() / self.spectrum.histogram.Integral()

    def draw(self):
        self.canvas_name = self.histogram.GetName() + "_canvas"
        self.canvas = ROOT.TCanvas(self.canvas_name, self.canvas_name)
        self.canvas.cd()
        self.histogram.Draw()
        self.pave.Draw()
        self.canvas.Update()

if __name__ == '__main__':
    spectrum = Spectrum("spekcalc_end100.dat")
    detector = DetectorEfficiency(14, 0.8)
    dead_layer = Transmission(14, 0.15)

    fixed_part = spectrum + detector + dead_layer
    
    filtering_elements = {
            "tungsten": Transmission(74, 0.03),
            }

    fixed_part.draw()
    window = 50, 75
    f = Filter(fixed_part, filtering_elements, window)
    f.filter()
    raw_input()
