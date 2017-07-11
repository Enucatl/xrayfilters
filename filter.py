#!/usr/bin/env python

"""Calculate the spectrum and the visibility after passing some filters.

"""
from __future__ import division, print_function

import random
import string
import os
import numpy as np

from transmission import Visibility, Spectrum, Transmission, DetectorEfficiency


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
        self.histogram = np.copy(spectrum.histogram)
        self._visibility = visibility
        
    def filter(self, change_thickness_of={}):
        if not self.tr_dict:
            return
        else:
            for key, new_thickness in change_thickness_of.items():
                self.tr_dict[key].thickness = new_thickness
            print(list(self.tr_dict.values())[0].histogram.shape)
            total_filter = sum(
                list(self.tr_dict.values())[1:],
                list(self.tr_dict.values())[0])
            print(total_filter.histogram.shape)
            self.histogram = np.copy(self.spectrum.histogram)
            self.histogram[:, 1] *= total_filter.histogram[:, 1]
            element_thickness = ("{0}, {1:.4f} #(){{cm}}".format(
                tr.element, tr.thickness)
                for tr in self.tr_dict.values())

    def visibility(self):
        temp_hist = np.copy(self.histogram)
        temp_hist *= self._visibility.histogram
        return np.sum(temp_hist) / np.sum(self.histogram)

    def efficiency(self):
        return np.sum(self.histogram) / np.sum(self.spectrum.histogram)


if __name__ == '__main__':
    import argparse
    commandline_parser = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    commandline_parser.add_argument('--spectrum', '-s',
            metavar='FILE',
            nargs=1,
            help='''File with the spekcalc spectrum.''')
    commandline_parser.add_argument('--energy', '-e',
            type=float,
            nargs='?',
            default=100,
            help='design energy of the interferometer (keV).')
    commandline_parser.add_argument('--talbot', '-t',
            type=int, metavar='ORDER',
            nargs='?',
            default=1,
            help='fractional Talbot distance.')
    commandline_parser.add_argument('--filters', '-f',
            nargs='*', metavar='ELEMENT/DENSITY/THICKNESS',
            help='''filters with the syntax
            element/density(g/cm3)/thickness(cm), e.g. 300 um of
            Tungsten can be passed as --filters W/19.25/0.03 .''')

    args = commandline_parser.parse_args()

    spectrum = Spectrum(args.spectrum[0])
    target_energy = args.energy
    talbot_order = args.talbot

    filtering_elements = [x.split('/') for x in args.filters]
    filtering_elements = [(element.capitalize(),
                           float(density), float(thickness))
        for element, density, thickness in filtering_elements]
    filtering_elements = dict([(element, Transmission(
        element, thickness, density, spectrum.min_energy,
        spectrum.max_energy))
        for element, density, thickness in filtering_elements])

    visibility = Visibility(
        spectrum.min_energy, spectrum.max_energy,
        target_energy, talbot_order)
    f = Filter(spectrum, filtering_elements, visibility)
    f.filter()
    input()
