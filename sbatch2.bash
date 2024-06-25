#!/bin/bash 

#SBATCH --job-name="nt-parallel" 

#SBATCH --output="nt-parallel.%j.%N.out" 

#SBATCH --partition=shared

#SBATCH --nodes=1 

#SBATCH --ntasks-per-node=64

#SBATCH --cpus-per-task=1

#SBATCH --account=ccu108 

#SBATCH --export=ALL 

#SBATCH -t 00:45:00

module purge 
module load slurm
module load cpu/0.17.3b
module load gcc/10.2.0/npcyll4
module load openmpi/4.1.1

# Constants for the simulation
C=1.0
A=0.1
H=20.0
# Define the specific neutron counts
neutron_counts=(85000000 90000000 95000000 100000000 150000000)

# Loop through neutron counts and process counts from 1 to 64
for n in "${neutron_counts[@]}"; do
    for p in $(seq 1 64); do
        echo "Running simulation with N=$n, P=$p, C=$C, A=$A, H=$H"
        # Use srun to execute the program and capture the specific output
        output=$(srun --mpi=pmix --ntasks=$p ./nt-parallel -C $C -A $A -H $H -n $n)
        overall_time=$(echo "$output" | grep "Overall Time" | awk '{print $3}')
        echo "N=$n, P=$p, Overall Time: $overall_time seconds" >> neutron_sim_${SLURM_JOB_ID}.out
    done
done