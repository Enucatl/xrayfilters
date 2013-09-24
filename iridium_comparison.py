from filter import Filter
from transmission import Spectrum, Transmission, DetectorEfficiency

spectrum = Spectrum("spekcalc_end100.dat")
detector = DetectorEfficiency(14, 0.8)
dead_layer = Transmission(14, 0.15)

fixed_part = spectrum + detector + dead_layer
window = 50, 75
    
filtering_elements1 = {
        "iridium": Transmission(77, 0.0220),
        }

filtering_elements2 = {
        "iridium": Transmission(77, 0.0200),
        "iron": Transmission(26, 0.0200),
        "copper": Transmission(29, 0.0080),
        }

f1 = Filter(fixed_part, filtering_elements1, window)
f2 = Filter(fixed_part, filtering_elements2, window)

f1.filter()
f2.filter()

f1.draw()
f2.draw()
raw_input()
