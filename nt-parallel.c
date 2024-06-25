#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <mpi.h>
#include <time.h>
#include <string.h>


double uniformRandom(unsigned short seed[3]) {
    return erand48(seed); // Use erand48() with the seed array
}

int main(int argc, char *argv[]) {
    int rank, size;


    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc == 1 || (argc == 2 && (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help")))) {
        if (rank == 0) {
            fprintf(stderr, "Usage: %s -C <double> -A <double> -H <double> -n <int>\n", argv[0]);
        }
        MPI_Finalize();
        return 0;
    }

    MPI_Barrier(MPI_COMM_WORLD); // Ensure all processes start timing at roughly the same time
    double startOverall = MPI_Wtime();

    // Seed initialization using rank to ensure uniqueness
    time_t now = time(NULL);
    unsigned short seed[3];
    seed[0] = (now & 0xFFFF) ^ (rank & 0xFFFF); // Combine time and rank, then XOR to fit in unsigned short
    seed[1] = (now >> 16) ^ (rank >> 8);        // Shift and spread bits of time and rank for diversity
    seed[2] = getpid(); 

    int opt, n = -1;
    double C = -1, Cs = -1, Cc = -1, H = -1;

    // Command-line argument parsing
    // Only process 0 needs to parse the command-line arguments
    if (rank == 0) {
        while ((opt = getopt(argc, argv, "C:A:H:n:")) != -1) {
            switch (opt) {
                case 'C':
                    C = atof(optarg);
                    break;
                case 'A':
                    Cc = atof(optarg);
                    Cs = C - Cc; // Assuming Cs + Cc = C
                    break;
                case 'H':
                    H = atof(optarg);
                    break;
                case 'n':
                    n = atoi(optarg);
                    break;
                default:
                    fprintf(stderr, "Usage: %s -A absorbtion -C mean_free_path -H thickness -n samples\n", argv[0]);
                    MPI_Abort(MPI_COMM_WORLD, 1);
            }
        }
    }

    // Broadcast the parameters to all processes
    MPI_Bcast(&C, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&Cc, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&H, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    if (n <= 0) {
        fprintf(stderr, "n must be > 0\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    // Adjust n for the number of processes
    int local_n = n / size; // Base count of neutrons per process
    int r = 0, b = 0, t = 0;

    // Simulation
    for (int i = 0; i < local_n; ++i) {
        // Your simulation code here, using uniformRandom(seed)
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

    // Collect results using MPI_Reduce
    int total_r, total_b, total_t;
    MPI_Reduce(&r, &total_r, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    MPI_Reduce(&b, &total_b, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    MPI_Reduce(&t, &total_t, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    MPI_Barrier(MPI_COMM_WORLD);
    double endOverall = MPI_Wtime();

    // Calculate the elapsed time
    double elapsedOverall = endOverall - startOverall;

    if (rank == 0) {
        // Only the master process prints the final results
        printf("reflected (r) = %d, absorbed (b) = %d, transmitted (t) = %d\n", total_r, total_b, total_t);
        printf("r/n = %.5f, b/n = %.5f, t/n = %.5f\n", total_r/(double)n, total_b/(double)n, total_t/(double)n);
        printf("Overall Time: %.6f seconds\n", elapsedOverall);
    }

    MPI_Finalize();


    return 0;
}
