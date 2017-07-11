from math import pi, sin, fabs
import os
import numpy as np
import scipy.interpolate
import nist_lookup.xraydb_plugin as xraydb


class Visibility(object):
    """Calculate the polychromatic visibility as in Thuering 2013,
    Performance and optimization of X-ray grating interferometry
    
    the visibility for a pi-shifting G1, target energy of E_0,
    and a fractional Talbot order m is given by

        v(E) = \\frac{2}{\pi}
                    \left | \sin^2(\pi E_0 / E) \sin (m\pi / 2 E_0/E)\\right |

    The total visibility is then the integral of v(E) weighted over the
    spectrum.
    """
    def __init__(self,
            min_energy=10, max_energy=200,
            target_energy=100,
            talbot_order=1):
        super(Visibility, self).__init__()
        self._target_energy = target_energy
        self._talbot_order = talbot_order
        self.histogram = np.vstack(zip(
            np.arange(min_energy, max_energy + 1),
            np.zeros(max_energy + 1 - min_energy)))
        for i, energy in enumerate(range(min_energy, max_energy + 1)):
            visibility = 2 / pi * fabs(sin(pi / 2 * self._target_energy /
                energy)**2 * sin(self._talbot_order * pi / 2 *
                    self._target_energy / energy))
            self.histogram[i, 1] = visibility


class Transmission(object):
    """the Transmission object is a histogram with the transmission exp(-mu
    x) as a function of energy. The thickness x can be changed as a python
    property.
    All measures of length are in cm!"""

    def __init__(self, element, density, thickness=1, min_energy=10, max_energy=200):
        super(Transmission, self).__init__()
        self.element = element
        self.histogram = np.vstack(zip(
            np.arange(min_energy, max_energy + 1),
            np.zeros(1 + max_energy - min_energy)))
        self.min_energy = min_energy
        self.max_energy = max_energy
        for i, energy in enumerate(range(min_energy, max_energy + 1)):
            _, _, atlen = xraydb.xray_delta_beta(
                element, density, energy * 1e3)
            self.histogram[i, 1] = np.exp(-1 / atlen)
        self.graph = scipy.interpolate.interp1d(
            self.histogram[:, 0],
            self.histogram[:, 1],
            fill_value="extrapolate")
        self.thickness = thickness

    def get_thickness(self):
        return self._thickness

    def set_thickness(self, thickness):
        """calculate transmission according to the thickness (cm) of the
        filter"""
        self._thickness = thickness

        for i, energy in enumerate(range(self.min_energy, self.max_energy +
                                        1)):
            transmission = self.graph(energy)
            if transmission > 0:
                transmission = transmission ** thickness
            else:
                transmission = 0
            self.histogram[i, 1] = transmission

    thickness = property(get_thickness, set_thickness)

    def __add__(self, other):
        self.histogram[:, 1] *= other.histogram[:, 1]
        return self


class DetectorEfficiency(Transmission):
    """photons absorbed in the detector"""
    def __init__(self, *args, **kwargs):
        super(DetectorEfficiency, self).__init__(*args, **kwargs)

    def set_thickness(self, thickness):
        """calculate efficiency according to the thickness (cm) of the
        filter"""
        self._thickness = thickness
        "evaluate efficiency in steps of 1 keV"
        for i, energy in enumerate(range(self.min_energy, self.max_energy +
                                        1)):
            transmission = self.graph(energy)
            if transmission > 0:
                transmission = 1 - transmission ** thickness
            else:
                transmission = 1
            self.histogram[i, 1] = transmission


class Spectrum(Transmission):
    """read spectrum from spekcalc file"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.histogram = np.genfromtxt(file_name)
        self.min_energy = int(self.histogram[0, 0])
        self.max_energy = int(self.histogram[-1, 0])


if __name__ == '__main__':
    import sys
    gold = Transmission("Au", 0.1)
    lead = Transmission("Pb", 0.1)
    double = gold + lead
    spectrum = Spectrum(sys.argv[1])
    print(spectrum.histogram)
    print(
        "mean energy:",
        np.dot(spectrum.histogram[:, 0],
               spectrum.histogram[:, 1]) /
        np.sum(spectrum.histogram[:, 1]), "keV")
