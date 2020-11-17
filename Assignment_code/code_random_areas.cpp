/* This code produces a text file with areas of the Mandelbrot set calculated
 * with 100,000 samples, 100 iterations per sample and 10,000 simulations*/

#include <iostream>
#include <complex>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <fstream>

using namespace std;

// Generates a candidate for the mandelbrot set
complex<double> generate_candidate(double start_x , double end_x, double start_y, double end_y){
    float r_1 = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    float r_2 = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    double imag = r_1 * (end_y - start_y) + start_y;
    double real = r_2 * (end_x - start_x) + start_x;
    std::complex<double> x(real, imag);
    return x;
}



// Determines whether or not a point is in the mandelbrot set
bool is_mandelbrot(complex<double> candidate, int iterations) {
    complex<double> squared;
    complex<double> sum = 0;
    for (int i = 0; i < iterations; i++) {
        squared = pow(sum, 2);
        sum = squared + candidate;
        // Check boundaries
        if (sum.real() > 2 || sum.real() < -2 || sum.imag() < -2 || sum.imag() > 2) {
            return false;
        }
    }
    return true;
}

int main(){
    // Do 100,000 samples every batch
    int samples =  100000;
    int iterations = 100;
    int count = 0;
    int repetitions = 10000;
    std:: complex<double> candidate;

    ofstream myfile;
    myfile.open ("random_many.txt");
    for (int j = 1; j < repetitions; j ++) {
        for (int i = 1; i < samples; i++) {
            candidate = generate_candidate(-2, 1, -1, 1);
            if (is_mandelbrot(candidate, iterations)) {
                count += 1;
            }
        }
        myfile << count << std::endl;
        count = 0;
    }
    myfile.close();
}