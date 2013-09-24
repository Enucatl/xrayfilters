"""
Get and save the linear attenuation coefficient tables from nist.gov
"""

from __future__ import division, print_function
from string import Template
from rootstyle import tdrstyle
from BeautifulSoup import BeautifulSoup
import os
import urllib2
import ROOT
import math

template_url = Template(
        "http://physics.nist.gov/cgi-bin/ffast/ffast.pl?\
Z=$Z&Formula=&gtype=5&range=S\
&lower=$lower_energy&upper=$upper_energy\
&density=&frames=no&htmltable=1")

tdrstyle()

class AttenuationTable(object):
    """get and save the linear attenuation coefficient table for given
    element and energy range (keV)"""
    def __init__(self, element_Z, min_energy=10, max_energy=200):
        super(AttenuationTable, self).__init__()
        self.element_Z = element_Z
        self.min_energy = min_energy
        self.max_energy = max_energy
        self.url = template_url.safe_substitute(
                Z=element_Z,
                lower_energy=min_energy,
                upper_energy=max_energy
                )
        self.get_table()

    def get_table(self):
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup(page.read())
        table = soup.find("table")
        rows = table.findAll("tr")
        self.table = []
        for row in rows:
            cols = row.findAll("td")
            table_row = []
            for cell in cols:
                content = cell.find(text=True).replace("&nbsp;", "")
                table_row.append(content)
            self.table.append(table_row)

    def save_tables(self, folder="."):
        self.file_name = os.path.join(folder,
                "linear_attenuation_{0}_{1}_{2}".format(
                    self.element_Z,
                    self.min_energy,
                    self.max_energy))
        with open(self.file_name, "w") as out_file:
            for row in self.table:
                for column in row:
                    print(column, end=" ", file=out_file)
                print("", file=out_file)
        self.save_transmission_table(folder)

    def save_transmission_table(self, folder="."):
        """save
        E (keV) | exp(-mu)

        table with transmission coefficients"""
        self.transmission_file_name = os.path.join(
                folder,
                "transmission_{0}_{1}_{2}".format(
                    self.element_Z,
                    self.min_energy,
                    self.max_energy))
        with open(self.transmission_file_name, "w") as out_file:
            for row in self.table:
                if not row:
                    continue
                energy = row[0]
                attenuation = float(row[1])
                transmission = str(math.exp(-attenuation))
                print(energy, transmission, file=out_file)
                print("", file=out_file)

    def draw(self):
        self.canvas = ROOT.TCanvas(self.file_name, self.file_name)
        self.canvas.SetLogy()
        self.graph = ROOT.TGraph(self.file_name)
        self.graph.SetTitle("linear attenuation coefficient for Z = {0};\
X ray energy #(){{keV}};\
Z = {0}    #mu #(){{cm^{{-1}}}}".format(self.element_Z))
        self.graph.Draw("al")

if __name__ == '__main__':
    a = AttenuationTable(79)
    a.draw()
    a.save_tables()
    input()
