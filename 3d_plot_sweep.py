import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_3d_surface(csv_file_path):
    # Load the data from CSV
    data = pd.read_csv(csv_file_path)

    # Create pivot tables for each fraction
    reflected_pivot = data.pivot(index='A', columns='H', values='Reflected').fillna(0)
    absorbed_pivot = data.pivot(index='A', columns='H', values='Absorbed').fillna(0)
    transmitted_pivot = data.pivot(index='A', columns='H', values='Transmitted').fillna(0)

    # Generate a meshgrid for A and H values
    A_unique = np.sort(data['A'].unique())
    H_unique = np.sort(data['H'].unique())
    A, H = np.meshgrid(H_unique, A_unique)

    # Plot each 3D surface
    fig = plt.figure(figsize=(18, 5))

    # Plot reflected
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot_surface(A, H, reflected_pivot.values / 1000, cmap='viridis')
    ax1.set_title('Reflected')
    ax1.set_xlabel('H')
    ax1.set_ylabel('A')
    ax1.set_zlabel('r/n')

    # Plot absorbed
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.plot_surface(A, H, absorbed_pivot.values / 1000, cmap='magma')
    ax2.set_title('Absorbed')
    ax2.set_xlabel('H')
    ax2.set_ylabel('A')
    ax2.set_zlabel('b/n')

    # Plot transmitted
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot_surface(A, H, transmitted_pivot.values / 1000, cmap='coolwarm')
    ax3.set_title('Transmitted')
    ax3.set_xlabel('H')
    ax3.set_ylabel('A')
    ax3.set_zlabel('t/n')

    # Adjust layout to make room for plots and remove extra white space
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    # Save the plot to a PNG file
    plt.savefig('neutron_interaction_3d.png')
    plt.show()

# Usage
csv_file_path = 'data_for_paper/sweep_data.csv'  # Replace with the path to your CSV file
plot_3d_surface(csv_file_path)
