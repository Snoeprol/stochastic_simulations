#include <iostream>
#include <complex>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <fstream>

#include "mt19937.h"
#include "rand_support.h"
#include "ortho-sampling.h"

using namespace std;

// Structure for saving if a point is in the Mandelbrot set with the iterations
struct mandelStruct
{
    int iterations;
    bool in_mandelbrot;
};

// Generates a candidate for the mandelbrot set
complex<double> generate_candidate(double start_x , double end_x, double start_y, double end_y){
    float r_1 = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    float r_2 = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    double imag = r_1 * (end_y - start_y) + start_y;
    double real = r_2 * (end_x - start_x) + start_x;
    std::complex<double> x(real, imag);
    return x;
}

// Given the pixels and intervals generates a candidate for the mandelbrot set
complex<double> generate_from_pixels(int x_pixel, int y_pixel, int x_interval, int y_interval){
    double x_coord = (double) x_pixel/x_interval * 3 - 2;
    double y_coord = (double) y_pixel/y_interval * 2 - 1;
    std::complex<double> candidate(x_coord, y_coord);
    return candidate;
}

// Determines whether or not a point is in the mandelbrot set
mandelStruct is_mandelbrot_struct(complex<double> candidate, int iterations) {

    complex<double> squared;
    complex<double> sum = 0;
    mandelStruct mandel;
    for (int i = 0; i < iterations; i++) {
        squared = pow(sum, 2);
        sum = squared + candidate;
        mandel.iterations = i;
        // Check boundaries
        if (sum.real() > 2 || sum.real() < -2 || sum.imag() < -2 || sum.imag() > 2) {
            mandel.in_mandelbrot = false;
            return mandel;
        }

    }
    mandel.in_mandelbrot = true;
    return mandel;
}

// Determines sampling uniformly over a set of pixels
int data_from_pixels(){

    // Samples
    int iterations = 100;

    // set seed
    srand (time(NULL));

    // x_pixels
    int x_pixels = 10000;
    //y_pixels
    int y_pixels = 10000;

    ofstream myfile;
    myfile.open ("numbers.txt");
    myfile << "real , imag, in_mandelbrot\n";
    for (int i = 0; i < x_pixels; i++) {
        for (int j = 0; j < y_pixels; j++) {
            complex<double> candidate = generate_from_pixels(i, j, x_pixels, y_pixels);
            auto mandel = is_mandelbrot_struct(candidate, iterations);
            myfile << i << "," << j << "," << std::boolalpha << mandel.in_mandelbrot << ","
                   << mandel.iterations << "\n";
        }
    }
    myfile.close();
    return 0;
}

// Random sampling
int data_from_random(){

    // Samples
    int iterations = 100;
    int samples =  10000;

    // set seed
    srand (time(NULL));

    // x_pixels
    int x_pixels = 10000;
    //y_pixels
    int y_pixels = 10000;

    ofstream myfile;
    myfile.open ("numbers.txt");
    myfile << "real , imag, in_mandelbrot\n";
    for (int i = 0; i < samples; i++) {
            complex<double> candidate = generate_candidate(-2, 1, -1, 1);
            auto mandel = is_mandelbrot_struct(candidate, iterations);
            myfile << candidate.real() << "," << candidate.imag() << "," << std::boolalpha << mandel.in_mandelbrot << ","
                   << mandel.iterations << "\n";
        }
    myfile.close();
    return 0;
}

// Uses orthogonal sampling to generate data
int data_from_orthogonal(){

    // Samples per cube and cubes
    int iterations = 100;
    int samples_per_cube =  10000;
    int x_cubes = 10;
    int y_cubes = 10;
    double y_interval = 2;
    double x_interval = 3;
    // set seed
    srand (time(NULL));


    ofstream myfile;
    myfile.open ("numbers.txt");
    myfile << "real , imag, in_mandelbrot\n";
    for (int i = 0; i < x_cubes; i++){
        double start_x = i/x_cubes * x_interval - 2;
        double end_x = (i + 1)/x_cubes * x_interval - 2;
        for (int j = 0; i < y_cubes; j++){
            double start_y = j/y_cubes * y_interval - 1;
            double end_y = (j + 1)/y_cubes * y_interval - 1;
            for (int k = 0; i < samples_per_cube; k++){

                complex<double> candidate = generate_candidate(start_x, end_x, start_y, end_y);
                auto mandel = is_mandelbrot_struct(candidate, iterations);
                myfile << candidate.real() << "," << candidate.imag() << "," << std::boolalpha << mandel.in_mandelbrot << ","
                       << mandel.iterations << "\n";
            }
        }
    }

    myfile.close();
    return 0;
}

int data_from_latin_hypercube(){
    //candidates = generate_candidates();
    return 0;
}


int main(){
    //orthogonal_sample();
}

