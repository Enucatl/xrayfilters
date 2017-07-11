#!/usr/bin/env python
from __future__ import division, print_function

import math
from pygene3.gene import FloatGene
from pygene3.organism import Organism
from pygene3.population import Population
from filter import Filter
from transmission import Spectrum, Transmission, DetectorEfficiency, Visibility
import sys

try:
    spectrum = Spectrum(sys.argv[1])
except IndexError:
    spectrum = Spectrum("spekcalc_end100.dat")

detector = DetectorEfficiency(
    "Si", 2.33, 0.8,
    spectrum.min_energy,
    spectrum.max_energy)
dead_layer = Transmission(
    "Al", 2.7, 0.15,
    spectrum.min_energy,
    spectrum.max_energy)
fixed_part = spectrum + detector + dead_layer
design_energy = 45
talbot_order = 1
visibility = Visibility(
    spectrum.min_energy, spectrum.max_energy,
    design_energy, talbot_order)

#thomas' setup
#filter_frame = Transmission(22, 0.0240)
#fixed_part = spectrum + filter_frame

densities = {
"Fe": 7.96,
"Cu": 8.92,
"Mo": 10.28,
"Nd": 6.8,
"Ir": 22.65,
}

class ThicknessGene(FloatGene):

    "genes randomly generated within this range"
    """max and min thickness"""
    randMin = 0
    randMax = 0.0200
        
    "probability of mutation"
    mutProb = 0.2

    "amplitude of mutation as a fraction of the current value"
    mutAmt = 0.05


class LivingFilter(Organism, Filter):
    """fixed part (detector + tube spectrum) taken as global variables"""

    element_list = [
        #"Al",
        "Fe",
        "Cu",
        "Mo",
        "Nd",
        #"Pb",
        #"W",
        "Ir",
    ]

    genome = dict(
            (element, ThicknessGene)
            for element in element_list)

    def __init__(self, **kwargs):
        Organism.__init__(self, **kwargs)
        tr_dict = dict(
            (element, Transmission(element, densities[element], 0,
                                   spectrum.min_energy, spectrum.max_energy))
            for element in self.genes)
        Filter.__init__(self, fixed_part, tr_dict, visibility)
        self.filter()

    def filter(self):
        change_thickness_of = dict(
                (name, gene.value)
                for name, gene in self.genes.items())
        Filter.filter(self, change_thickness_of)

    def fitness(self):
        return self.visibility()

    def prepare_fitness(self):
        self.filter()
        Organism.prepare_fitness(self)

    def __add__(self, other):
        child1, child2 = Organism.__add__(self, other)
        child1.filter()
        child2.filter()
        return child1, child2

    def mutate(self):
        return Organism.mutate(self)

class FilterPopulation(Population):
    """population of filters"""
    species = LivingFilter
    initPopulation = 20

    " cull to this many children after each generation"
    childCull = 5

    " number of children to create after each generation"
    childCount = 50

if __name__ == '__main__':
    print("parameters:")
    print("fixed frame", fixed_part)
    pop = FilterPopulation()
    try:
        generations = 0
        while True:
            # execute a generation
            pop.gen()
            generations += 1

            best = pop.organisms[0]
            #best.draw()
            print("fitness={0}".format(best.get_fitness()))
            #for name, gene in best.genome.items():
                #print(name, gene.value)
            print("generation", generations)

    except KeyboardInterrupt:
        pass
    print("Executed", generations, "generations")
    # pop.organisms[0].draw()
    input()
