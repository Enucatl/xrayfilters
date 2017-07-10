#!/usr/bin/env python
from __future__ import division, print_function

import math
from periodic_table import periodic_table, name_to_Z
from pygene.gene import FloatGene
from pygene.organism import Organism
from pygene.population import Population
from filter import Filter
from transmission import Spectrum, Transmission, DetectorEfficiency, Visibility
import sys

try:
    spectrum = Spectrum(sys.argv[1])
except IndexError:
    spectrum = Spectrum("spekcalc_end100.dat")

detector = DetectorEfficiency(14, 0.8)
dead_layer = Transmission(14, 0.15)
energy_window = 50, 75
fixed_part = spectrum + detector + dead_layer

#thomas' setup
#energy_window = 21, 41
#filter_frame = Transmission(22, 0.0240)
#fixed_part = spectrum + filter_frame

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
            #"Aluminium",
            "Iron",
            "Copper",
            "Germanium",
            "Molybdenum",
            "Neodymium",
            #"Cerium",
            #"Lead",
            #"Tungsten",
            "Iridium",
            ]

    genome = dict(
            (element, ThicknessGene)
            for element in element_list)

    def __init__(self, **kwargs):
        Organism.__init__(self, **kwargs)
        tr_dict = dict(
            (gene, Transmission(name_to_Z[gene], 0))
            for gene in self.genes)
        Filter.__init__(self, fixed_part, tr_dict, energy_window)
        self.filter()

    def filter(self):
        change_thickness_of = dict(
                (name, gene.value)
                for name, gene in self.genes.items())
        Filter.filter(self, change_thickness_of)

    def fitness(self):
        bad_purity = 1 - self.purity()
        return bad_purity

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
    print("energy window (keV)", energy_window)
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
    pop.organisms[0].draw()
    raw_input()


