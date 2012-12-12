#include<TGraph.h>
#include <TH1.h>
#include <cmath>

void update_histogram(const TGraph& graph, TH1D& histogram, double thickness, int min, int max){
    double transmission = 0;
    for (int energy = min; energy < max; energy++) {
        transmission = graph.Eval(energy, 0, "S");
        if (transmission > 0) {
            transmission = pow(transmission, thickness);
        }
        else {
            transmission = 0;
        }
        histogram.SetBinContent(energy - min + 1, transmission);
    }
}
