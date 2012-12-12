periodic_table = {
1: 'Hydrogen',
2: 'Helium',
3: 'Lithium',
4: 'Beryllium',
5: 'Boron',
6: 'Carbon',
7: 'Nitrogen',
8: 'Oxygen',
9: 'Fluorine',
10: 'Neon',
11: 'Sodium',
12: 'Magnesium',
13: 'Aluminium',
14: 'Silicon',
15: 'Phosphorus',
16: 'Sulfur',
17: 'Chlorine',
18: 'Argon',
19: 'Potassium',
20: 'Calcium',
21: 'Scandium',
22: 'Titanium',
23: 'Vanadium',
24: 'Chromium',
25: 'Manganese',
26: 'Iron',
27: 'Cobalt',
28: 'Nickel',
29: 'Copper',
30: 'Zinc',
31: 'Gallium',
32: 'Germanium',
33: 'Arsenic',
34: 'Selenium',
35: 'Bromine',
36: 'Krypton',
37: 'Rubidium',
38: 'Strontium',
39: 'Yttrium',
40: 'Zirconium',
41: 'Niobium',
42: 'Molybdenum',
43: 'Technetium',
44: 'Ruthenium',
45: 'Rhodium',
46: 'Palladium',
47: 'Silver',
48: 'Cadmium',
49: 'Indium',
50: 'Tin',
51: 'Antimony',
52: 'Tellurium',
53: 'Iodine',
54: 'Xenon',
55: 'Caesium',
56: 'Barium',
71: 'Lutetium',
72: 'Hafnium',
73: 'Tantalum',
74: 'Tungsten',
75: 'Rhenium',
76: 'Osmium',
77: 'Iridium',
78: 'Platinum',
79: 'Gold',
80: 'Mercury',
81: 'Thallium',
82: 'Lead',
83: 'Bismuth',
84: 'Polonium',
85: 'Astatine',
86: 'Radon',
87: 'Francium',
88: 'Radium',
103: 'Lawrencium',
104: 'Rutherfordium',
105: 'Dubnium',
106: 'Seaborgium',
107: 'Bohrium',
108: 'Hassium',
109: 'Meitnerium',
110: 'Darmstadtium',
111: 'Roentgenium',
112: 'Copernicium',
113: 'Ununtrium',
114: 'Ununquadium',
115: 'Ununpentium',
116: 'Ununhexium',
117: 'Ununseptium',
118: 'Ununoctium',
57: 'Lanthanum',
58: 'Cerium',
59: 'Praseodymium',
60: 'Neodymium',
61: 'Promethium',
62: 'Samarium',
63: 'Europium',
64: 'Gadolinium',
65: 'Terbium',
66: 'Dysprosium',
67: 'Holmium',
68: 'Erbium',
69: 'Thulium',
70: 'Ytterbium',
89: 'Actinium',
90: 'Thorium',
91: 'Protactinium',
92: 'Uranium',
93: 'Neptunium',
94: 'Plutonium',
95: 'Americium',
96: 'Curium',
97: 'Berkelium',
98: 'Californium',
99: 'Einsteinium',
100: 'Fermium',
101: 'Mendelevium',
102: 'Nobelium',
}

name_to_Z = {
'Hydrogen': 1,
'Helium': 2,
'Lithium': 3,
'Beryllium': 4,
'Boron': 5,
'Carbon': 6,
'Nitrogen': 7,
'Oxygen': 8,
'Fluorine': 9,
'Neon': 10,
'Sodium': 11,
'Magnesium': 12,
'Aluminium': 13,
'Silicon': 14,
'Phosphorus': 15,
'Sulfur': 16,
'Chlorine': 17,
'Argon': 18,
'Potassium': 19,
'Calcium': 20,
'Scandium': 21,
'Titanium': 22,
'Vanadium': 23,
'Chromium': 24,
'Manganese': 25,
'Iron': 26,
'Cobalt': 27,
'Nickel': 28,
'Copper': 29,
'Zinc': 30,
'Gallium': 31,
'Germanium': 32,
'Arsenic': 33,
'Selenium': 34,
'Bromine': 35,
'Krypton': 36,
'Rubidium': 37,
'Strontium': 38,
'Yttrium': 39,
'Zirconium': 40,
'Niobium': 41,
'Molybdenum': 42,
'Technetium': 43,
'Ruthenium': 44,
'Rhodium': 45,
'Palladium': 46,
'Silver': 47,
'Cadmium': 48,
'Indium': 49,
'Tin': 50,
'Antimony': 51,
'Tellurium': 52,
'Iodine': 53,
'Xenon': 54,
'Caesium': 55,
'Barium': 56,
'Lutetium': 71,
'Hafnium': 72,
'Tantalum': 73,
'Tungsten': 74,
'Rhenium': 75,
'Osmium': 76,
'Iridium': 77,
'Platinum': 78,
'Gold': 79,
'Mercury': 80,
'Thallium': 81,
'Lead': 82,
'Bismuth': 83,
'Polonium': 84,
'Astatine': 85,
'Radon': 86,
'Francium': 87,
'Radium': 88,
'Lawrencium': 103,
'Rutherfordium': 104,
'Dubnium': 105,
'Seaborgium': 106,
'Bohrium': 107,
'Hassium': 108,
'Meitnerium': 109,
'Darmstadtium': 110,
'Roentgenium': 111,
'Copernicium': 112,
'Ununtrium': 113,
'Ununquadium': 114,
'Ununpentium': 115,
'Ununhexium': 116,
'Ununseptium': 117,
'Ununoctium': 118,
'Lanthanum': 57,
'Cerium': 58,
'Praseodymium': 59,
'Neodymium': 60,
'Promethium': 61,
'Samarium': 62,
'Europium': 63,
'Gadolinium': 64,
'Terbium': 65,
'Dysprosium': 66,
'Holmium': 67,
'Erbium': 68,
'Thulium': 69,
'Ytterbium': 70,
'Actinium': 89,
'Thorium': 90,
'Protactinium': 91,
'Uranium': 92,
'Neptunium': 93,
'Plutonium': 94,
'Americium': 95,
'Curium': 96,
'Berkelium': 97,
'Californium': 98,
'Einsteinium': 99,
'Fermium': 100,
'Mendelevium': 101,
'Nobelium': 102,
                }

