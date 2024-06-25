import subprocess
import csv
import sys
import os

# Check if an output file name was provided
if len(sys.argv) != 2:
    print("Usage: python3 gather_sweep_data.py <output_file_name>")
    sys.exit(1)

# Constants
C = 10.0
n = 1000
output_file_name = sys.argv[1]  # Use the command-line argument for the output file name

# Parameter ranges
A_values = [round(0.01 * i, 2) for i in range(1, 51)]
H_values = [round(0.01 * i, 2) for i in range(1, 1001)]

# Specify the relative path to the executable from the 'data' directory
executable_path = '../code/nt-serial'

# Make sure the script exists
if not os.path.isfile(executable_path):
    print(f"Error: Executable not found at {executable_path}")
    sys.exit(1)

# Open CSV file for writing results
with open(output_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['A', 'H', 'Transmitted', 'Absorbed', 'Reflected'])

    # Loop through each combination of A and H
    for A in A_values:
        for H in H_values:
            # Construct command to run the simulation
            command = [executable_path, f'-A {A}', f'-C {C}', f'-H {H}', f'-n {n}']
            # Execute the command
            result = subprocess.run(command, capture_output=True, text=True)
            if result.stderr:
                print(f'Error for A={A}, H={H}: {result.stderr}')
            # if result.stdout:
                # print(f'Output for A={A}, H={H}: {result.stdout}')
                lines = result.stdout.splitlines()
                try:
                    # Assuming the format is consistently given in the second line
                    data_line = lines[1]
                    values = {x.split('=')[0].strip(): float(x.split('=')[1]) for x in data_line.split(',')}
                    # Extract values
                    transmitted = values['t/n']
                    absorbed = values['b/n']
                    reflected = values['r/n']
                    # Write to CSV
                    writer.writerow([A, H, transmitted, absorbed, reflected])
                except Exception as e:
                    print(f'Failed to parse output for A={A}, H={H}: {e}')

print(f'Data collection complete. Results written to {output_file_name}')
