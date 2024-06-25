import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load your data
data = pd.read_csv('data_for_paper/performance2.csv')  # Adjust the path to your CSV file

# Unique values of N and P
N_values = data['N'].unique()
P_values = data['P'].unique()

# Function to plot graphs with distinct colors for each N value
def plot_graph_with_colors(y_label, ideal=None, ideal_label=None, filename_suffix=""):
    plt.figure(figsize=(10, 6))
    color_map = plt.cm.get_cmap('viridis', len(N_values))  # Using 'viridis' colormap for distinct colors
    
    for index, N in enumerate(N_values):
        subset = data[data['N'] == N]
        plt.plot(subset['P'], subset[y_label], label=f'N={N}', marker='o', color=color_map(index))
    
    if ideal is not None:
        plt.plot(P_values, ideal, 'k--', label=ideal_label)
    
    plt.xlabel('Number of Processes (P)')
    plt.ylabel(y_label)
    plt.title(f'{y_label} vs Number of Processes for Different N')
    plt.legend()
    plt.grid(True)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig(f'{filename_suffix}_with_colors_for_different_N.png')
    

# Generating and saving each graph
plot_graph_with_colors('Overall Time', ideal=np.zeros_like(P_values), ideal_label='Ideal (Y=0)', filename_suffix="timing")
plot_graph_with_colors('Speedup', ideal=P_values, ideal_label='Ideal (Y=X)', filename_suffix="speedup")
plot_graph_with_colors('Efficiency', ideal=np.ones_like(P_values), ideal_label='Ideal (Y=1)', filename_suffix="efficiency")
