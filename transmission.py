#!/usr/bin/env python
from __future__ import division, print_function
from rootstyle import tdrstyle
import math
import os
import ROOT

tdrstyle()

ROOT.gROOT.ProcessLine(".L update_histogram.C+")

class Visibility(object):
    """docstring for Visibility"""
    def __init__(self, min_energy=10, max_energy=200):
        super(Visibility, self).__init__()
        file_name = "visibility"
        histogram_name = file_name + "_hist"
        self.histogram = ROOT.TH1D(
                histogram_name,
                "visibility;\
X ray energy #(){keV};\
 arbitrary units",
                max_energy - min_energy,
                min_energy,
                max_energy)

        for i, energy in enumerate(range(min_energy, max_energy)):
            baseline = 0
            if energy < 50 or energy > 75:
                self.histogram.SetBinContent(i + 1, 1 - baseline)
            else:
                self.histogram.SetBinContent(i + 1,
                        1 - baseline + math.cos(math.pi * energy / 25 - 62.5));

class Transmission(object):
    """the Transmission object is a histogram with the transmission exp(-mu
    x) as a function of energy. The thickness x can be changed as a python
    property.
    All measures of length are in cm!"""

    def __init__(self, element_Z, thickness=1, min_energy=10, max_energy=200):
        super(Transmission, self).__init__()
        self.element_Z = element_Z
        folder = "nist"
        transmission_data_file_name = "transmission_{0}_{1}_{2}".format(
                element_Z,
                min_energy,
                max_energy)
        self.transmission_data_file_name = os.path.join(folder,
                transmission_data_file_name)
        if not os.path.exists(self.transmission_data_file_name):
            from nist.attenuation_table import AttenuationTable
            at = AttenuationTable(element_Z, min_energy, max_energy)
            at.save_tables(folder)
        self.canvas_name = "canvas_{0}_{1}_{2}_{3}".format(
                element_Z,
                min_energy,
                max_energy,
                thickness)
        histogram_name = self.transmission_data_file_name + "_hist"
        self.histogram = ROOT.TH1D(
                self.transmission_data_file_name + str(thickness),
                "transmission;\
X ray energy #(){{keV}};\
exp(- #mu x), Z = {0}, x = {1} #(){{cm}}".format(
    self.element_Z, thickness),
                max_energy - min_energy,
                min_energy,
                max_energy)
        self.min_energy = min_energy
        self.max_energy = max_energy
        self.graph = ROOT.TGraph(self.transmission_data_file_name)
        self.thickness = thickness

    def get_thickness(self):
        return self._thickness

    def set_thickness(self, thickness):
        """calculate transmission according to the thickness (cm) of the
        filter"""
        #self.histogram.SetTitle(
                #"transmission;\
#X ray energy #(){{keV}};\
#exp(- #mu x), Z = {0}, x = {1} #(){{cm}}".format(
    #self.element_Z, thickness))
        self._thickness = thickness

        "evaluate transmission in steps of 1 keV"
        ROOT.update_histogram(self.graph, self.histogram, thickness,
                self.min_energy, self.max_energy)
        #for i, energy in enumerate(xrange(self.min_energy, self.max_energy)):
            #transmission = self.graph.Eval(energy) 
            #if transmission > 0:
                #transmission = transmission ** thickness
            #else:
                #transmission = 0
            #self.histogram.SetBinContent(i + 1, transmission)

    thickness = property(get_thickness, set_thickness)

    def __add__(self, other):
        self.histogram.Multiply(other.histogram)
        return self

    def draw(self):
        self.canvas = ROOT.TCanvas(self.canvas_name, self.canvas_name)
        self.canvas.cd()
        self.histogram.Draw("l")
        self.canvas.Update()

class DetectorEfficiency(Transmission):
    """photons absorbed in the detector"""
    def __init__(self, *args, **kwargs):
        super(DetectorEfficiency, self).__init__(*args, **kwargs)

    def set_thickness(self, thickness):
        """calculate efficiency according to the thickness (cm) of the
        filter"""
        self._thickness = thickness
        "evaluate efficiency in steps of 1 keV"
        for i, energy in enumerate(range(self.min_energy, self.max_energy)):
            transmission = self.graph.Eval(energy) 
            if transmission > 0:
                transmission = 1 - transmission ** thickness
            else:
                transmission = 1
            self.histogram.SetBinContent(i + 1, transmission)

class Spectrum(Transmission):
    """read spectrum from spekcalc file"""
    def __init__(self, file_name, min_energy=10, max_energy=200):
        self.element_Z = 0
        self.min_energy = min_energy
        self.max_energy = max_energy
        self.file_name = file_name
        histogram_name = file_name + "_hist"
        self.canvas_name = "canvas_spectrum_{0}".format(
                file_name)
        self.histogram = ROOT.TH1D(
                histogram_name,
                "spectrum;\
X ray energy #(){keV};\
 #(){keV cm^{2} mA s}",
                max_energy - min_energy,
                min_energy,
                max_energy)
        with open(file_name) as in_file:
            for line in in_file:
                if "#" in line:
                    continue
                line = line.split()
                if len(line) is not 2:
                    continue
                try:
                    energy, value = int(line[0]), float(line[1])
                except ValueError:
                    continue
                i = int(energy - min_energy)
                if i < 0: continue
                self.histogram.SetBinContent(i + 1, value)

    def draw(self):
        self.canvas = ROOT.TCanvas(self.canvas_name, self.canvas_name)
        self.canvas.cd()
        self.histogram.Draw()
        self.canvas.Update()
        
if __name__ == '__main__':
    import sys
    gold = Transmission(79, 0.1)
    gold.draw()
    lead = Transmission(82, 0.1)
    lead.draw()
    double = gold + lead
    double.draw()
    spectrum = Spectrum(sys.argv[1])
    print("mean energy:", spectrum.histogram.GetMean(), "keV")
    spectrum.draw()
    raw_input()
