import sys
import subprocess
import numpy as np
import os

# Constants for the problem
C = 1.0
A = 0.1
H = 20.0
N_values = [85000000, 90000000, 95000000, 100000000, 150000000]
process_counts = range(1, 65)  

# Path to the executable
# Specify the relative path to the executable from the 'data' directory
executable_path = '../code/nt-parallel'
mpiexec_path = "mpiexec"

# Function to run the simulation
def run_simulation(processes, N):
    command = [mpiexec_path, "-n", str(processes), executable_path, "-C", str(C), "-A", str(A), "-H", str(H), "-n", str(N)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        # print(f"Error running with {processes} processes and N={N}: {result.stderr}")
        return None
    return result.stdout

# Main function to collect and process data
def main(output_file_name):
    results = []
    for N in N_values:
        times = []
        print(f"Testing for N={N}")
        for p in range(1, int(os.environ.get('SLURM_CPUS_PER_TASK')) + 1):  # Looping through 1 up to the number of CPUs requested per task
            output = run_simulation(p, N)
            if output is not None:
                lines = output.splitlines()
                time_line = next(line for line in lines if "Overall Time:" in line)
                time = float(time_line.split()[-2])
                times.append(time)
                # print(f"Processes: {p}, Time: {time} seconds")
            else:
                times.append(None)
        
        # Calculate speedup and efficiency
        base_time = times[0]  # Time with 1 process
        for i, time in enumerate(times):
            if time is not None:
                speedup = round(base_time / time, 6)
                efficiency = round(speedup / (i + 1), 6)
                results.append((N, i + 1, time, speedup, efficiency))
                # print(f"Processes: {i+1}, Speedup: {speedup}, Efficiency: {efficiency}")

    # Save results to a file
    np.savetxt(output_file_name, results, delimiter=",", fmt='%s', header="N,Processes,Time,Speedup,Efficiency")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gather_performance_data.py <output_file_name>")
        sys.exit(1)
    main(sys.argv[1])


