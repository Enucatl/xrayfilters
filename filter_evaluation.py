#!/usr/bin/env python
from __future__ import division, print_function

from filter import Filter
from transmission import Spectrum, Transmission, DetectorEfficiency
from rootstyle import tdrstyle
from subprocess import check_call
import ROOT
import sys
import os

tdrstyle()

if __name__ == '__main__':
    """base list is the filter given by the detector structure
    (dead layer and efficiency of the active layer)"""

    spectrum = Spectrum("spekcalc_end100.dat")
    detector = DetectorEfficiency(14, 0.8)
    dead_layer = Transmission(14, 0.15)

    fixed_part = spectrum + detector + dead_layer

    """element for the filter"""
    filter_Z = int(sys.argv[1])

    "energy window contributing to visibility in keV"
    min_energy = 50
    max_energy = 75

    "thickness always cm"
    min_thickness = 0.01
    max_thickness = 0.08
    thickness_step = 0.001
    number_of_steps = int(
            (max_thickness - min_thickness) / thickness_step)
    thickness_list = (min_thickness + i * thickness_step\
            for i in range(number_of_steps + 1))
    histogram_pars = number_of_steps, min_thickness, max_thickness

    "prepare histograms"
    efficiency_histogram_name = "efficiency_hist"
    efficiency_histogram = ROOT.TH1D(
            efficiency_histogram_name,
            "efficiency;Z = {0} thickness #(){{cm}};efficiency".format(
                filter_Z),
            *histogram_pars)

    purity_histogram_name = "purity"
    purity_histogram = ROOT.TH1D(
            purity_histogram_name,
            "purity;Z = {0} thickness @(){{cm}};purity {1}-{2} #(){{keV}}".format(
                filter_Z,
                min_energy,
                max_energy),
            *histogram_pars)


    "calculate efficiency/purity"
    filtering_with = Transmission(filter_Z, min_thickness)
    f = Filter(fixed_part, {filter_Z: filtering_with})
    memory = []
    canvases = {}
    draw_list = [0, number_of_steps - 1]
    for i, thickness in enumerate(thickness_list):
        f.filter({filter_Z: thickness})
        if i in draw_list or thickness == 0.03:
            f.draw()
            canvases[thickness] = f.canvas
            memory.append(f.histogram)
            memory.append(f.pave)
        efficiency = f.efficiency()
        purity = f.purity(min_energy, max_energy)
        efficiency_histogram.SetBinContent(i + 1, efficiency)
        purity_histogram.SetBinContent(i + 1, purity)


    "draw two histograms on the same canvas"
    transparent_canvas_name = "transparent_canvas"
    transparent_canvas = ROOT.TCanvas(transparent_canvas_name,
            transparent_canvas_name)
    efficiency_canvas_name = "efficiency_canvas"
    purity_canvas_name = "purity_canvas"
    efficiency_pad = ROOT.TPad(efficiency_canvas_name,
            efficiency_canvas_name, 0, 0, 1, 1)
    purity_pad = ROOT.TPad(purity_canvas_name,
            purity_canvas_name,
            0, 0, 1, 1)
    purity_pad.SetFillStyle(4000)
    efficiency_pad.Draw()
    efficiency_pad.cd()
    efficiency_histogram.Draw()
    efficiency_pad.Update()
    efficiency_histogram.Draw()
    transparent_canvas.cd()

    xmin = efficiency_pad.GetX1()
    xmax = efficiency_pad.GetX2()
    ymin = efficiency_pad.GetY1()
    ymax = efficiency_pad.GetY2()
    m = 1 / (ymax - ymin)
    ymin = (efficiency_pad.GetY1() - efficiency_pad.GetUymin()) * m
    ymax = 1 + (efficiency_pad.GetY2() - efficiency_pad.GetUymax()) * m
    efficiency_total_height = efficiency_pad.GetY2() - efficiency_pad.GetY1() 
    purity_total_height = ymax - ymin
    frame = purity_pad.Range(
            xmin,
            ymin,
            xmax,
            ymax,
            )
    purity_pad.Draw()
    purity_pad.cd()
    purity_histogram.SetLineColor(ROOT.kRed)
    purity_histogram.Draw("][same")
    purity_pad.Update()
    ymin_axis = ymin - (efficiency_pad.GetY1() - efficiency_pad.GetUymin()) * purity_total_height / efficiency_total_height
    ymax_axis = ymax - (efficiency_pad.GetY2() - efficiency_pad.GetUymax()) * purity_total_height / efficiency_total_height
    purity_axis = ROOT.TGaxis(
            efficiency_pad.GetUxmax(),
            ymin_axis,
            efficiency_pad.GetUxmax(),
            ymax_axis,
            0,
            1,
            510,
            "+L")
    purity_axis.SetTitle("purity")
    purity_axis.SetTitleColor(ROOT.kRed)
    purity_axis.SetLabelColor(ROOT.kRed)
    purity_axis.Draw()
    purity_pad.Update()

    "draw efficiency x purity as a 'merit figure'"
    product_canvas_name = "product_canvas"
    product_canvas = ROOT.TCanvas(product_canvas_name, product_canvas_name)
    product_histogram = efficiency_histogram.Clone("product")
    product_histogram.Multiply(purity_histogram)
    product_histogram.GetYaxis().SetTitle("efficiency #times purity")
    product_histogram.Draw()
    product_canvas.Update()

    "save images in plots folder"
    plot_folder = "plots"
    plot_format = ".pdf"
    file_name = "{0}_filter".format(filter_Z)
    file_name = os.path.join(plot_folder, file_name)
    transparent_canvas.SaveAs(file_name + "_eff_pur" + plot_format)
    product_canvas.SaveAs(file_name + "_product" + plot_format)
    for thickness, canvas in canvases.iteritems():
        canvas.SaveAs(file_name + "_spectrum_" + str(thickness) +
                plot_format)
    join_images_command = "pdftk {1}/{0}_filter*.pdf cat output {1}/{0}_joined.pdf".format(
            filter_Z, plot_folder)
    check_call(join_images_command, shell=True)
    #raw_input()
