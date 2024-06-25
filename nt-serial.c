#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <time.h>
#include "timer.h"


double uniformRandom(unsigned short seed[3]) {
    return erand48(seed); // Use erand48() with the seed array
}

int main(int argc, char *argv[]) {
    double startOverall, endOverall;
    double elapsedOverall;
    int opt;
    double C = -1, Cs = -1, Cc = -1, H = -1;
    int n = -1;
    GET_TIME(startOverall)
    // Use the current time to initialize the seed
    unsigned short seed[3];
    time_t now = time(NULL);
    seed[0] = now & 0xffff;                // Take the lower 16 bits
    seed[1] = (now >> 16) & 0xffff;        // Take the next 16 bits
    seed[2] = getpid() & 0xffff;  

    // Parse command-line arguments
    while ((opt = getopt(argc, argv, "C:A:H:n:")) != -1) {
        switch (opt) {
            case 'C':
                C = atof(optarg);
                Cs = C - Cc; // Assuming Cs + Cc = C
                break;
            case 'A':
                Cc = atof(optarg);
                break;
            case 'H':
                H = atof(optarg);
                break;
            case 'n':
                n = atoi(optarg);
                break;
            default:
                fprintf(stderr, "Usage: %s -A absorbtion -C mean_free_path -H thickness -n samples\n", argv[0]);
                exit(EXIT_FAILURE);

        }
    }

    if (Cc >= C || C <= 0 || H <= 0 || n <= 0) {
        fprintf(stderr, "A has to be less than C, all parameters > 0\n");
        exit(EXIT_FAILURE);
    }

    // Check if all parameters are set
    if (C < 0 || Cs < 0 || Cc < 0 || H < 0 || n < 0) {
        fprintf(stderr, "All parameters must be set.\n");
        fprintf(stderr, "Usage: %s -A absorbtion -C mean_free_path -H thickness -n samples\n", argv[0]);
        exit(EXIT_FAILURE);
    }

        // Variables to keep track of reflected, absorbed, and transmitted neutrons
    int r = 0, b = 0, t = 0;

    for (int i = 0; i < n; ++i) {
        double d = 0;
        double x = 0;
        int a = 1; // true

        while (a) { // While the particle is still bouncing
            double L = -1 / C * log(uniformRandom(seed));
            double u = uniformRandom(seed);
            x += L * cos(d);

            if (x < 0) {
                // Reflected
                ++r;
                a = 0; // false
            } else if (x > H) {
                // Transmitted
                ++t;
                a = 0; // false
            } else if (u < Cc / C) {
                // Absorbed
                ++b;
                a = 0; // false
            } else {
                // Otherwise, choose a new direction for the neutron
                d = u * M_PI;
            }
        }
    }

    GET_TIME(endOverall)

    elapsedOverall = endOverall-startOverall;
    

    // Printing the results
   // Display results
    printf("reflected (r) = %d, absorbed (b) = %d, transmitted (t) = %d\n", r, b, t);
    printf("r/n = %.5f, b/n = %.5f, t/n = %.5f\n", r/(double)n, b/(double)n, t/(double)n);
    printf("Overall Time: %.6f\n", elapsedOverall);
    return 0;
}
