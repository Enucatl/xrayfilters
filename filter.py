#!/usr/bin/env python

"""Calculate the spectrum and the visibility after passing some filters.

"""
from __future__ import division, print_function

import random
import string
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from transmission import Visibility, Spectrum, Transmission, DetectorEfficiency
from periodic_table import periodic_table, name_to_Z
from rootstyle import tdrstyle

tdrstyle()

class Filter(object):
    """the Filter is made of a Spectrum and one or more Transmission. The
    Spectrum also includes the detector and any fixed filters as well as a
    Visibility calculator. """

    def __init__(self, spectrum, tr_dict, visibility):
        super(Filter, self).__init__()
        max_energy = spectrum.max_energy
        min_energy = spectrum.min_energy
        self.spectrum = spectrum
        self.tr_dict = tr_dict
        histogram_name = " ".join(tr.histogram.GetName()
                for tr in self.tr_dict.itervalues())
        histogram_name += "".join(str(tr.thickness)
                for tr in self.tr_dict.itervalues())
        histogram_name += ''.join(random.choice(string.letters)
                for i in range(5))
        self.histogram = spectrum.histogram.Clone(histogram_name)
        self._visibility = visibility
        
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
            element_thickness = ("{0}, {1:.4f} #(){{cm}}".format(
                periodic_table[tr.element_Z], tr.thickness)
                for tr in self.tr_dict.itervalues())
            for element in element_thickness:
                self.pave.AddText(element)
            self.pave.SetFillColor(0)
            self.pave.AddText(
                    "total flux {0:.3g}".format(self.histogram.Integral()))
            self.pave.AddText("{0:.1%} efficiency".format(self.efficiency()))
            self.pave.AddText("{0:.1%} visibility".format(self.visibility()))

    def visibility(self):
        temp_hist = self.histogram.Clone()
        temp_hist.Multiply(self._visibility.histogram)
        return temp_hist.Integral() / self.histogram.Integral()

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
    import argparse
    commandline_parser = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    commandline_parser.add_argument('--spectrum', '-s',
            metavar='SPECTRUM_FILE',
            nargs=1,
            help='''File with the spekcalc spectrum.''')
    commandline_parser.add_argument('--energy', '-e',
            type=float,
            nargs='?',
            default=100,
            help='design energy of the interferometer (keV).')
    commandline_parser.add_argument('--talbot', '-t',
            type=int,
            nargs='?',
            default=1,
            help='fractional Talbot distance.')
    commandline_parser.add_argument('--filters', '-f',
            nargs='*',
            help='''filters with the syntax Element/thickness(cm), e.g. 300 um of
            Tungsten can be passed as --filters tungsten/0.03 .''')

    args = commandline_parser.parse_args()

    spectrum = Spectrum(args.spectrum[0])
    target_energy = args.energy
    talbot_order = args.talbot

    filtering_elements = [x.split('/') for x in args.filters]
    filtering_elements = [(element.capitalize(), float(thickness))
        for element, thickness in filtering_elements]
    filtering_elements = dict([(element, Transmission(name_to_Z[element], thickness))
        for element, thickness in filtering_elements])

    visibility = Visibility(spectrum.min_energy, spectrum.max_energy,
            target_energy, talbot_order)
    f = Filter(spectrum, filtering_elements, visibility)
    f.filter()
    f.draw()
    raw_input()
