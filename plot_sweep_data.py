import pandas as pd
import matplotlib.pyplot as plt

def plot_neutron_data(csv_file_path):
    # Load the data from CSV
    data = pd.read_csv(csv_file_path)

    # Sort data by thickness H for consistent plotting
    data.sort_values(by='H', inplace=True)

    # Plotting the data
    plt.figure(figsize=(10, 6))

    # Plot each fraction
    plt.plot(data['H'], data['Reflected']/1000, label='Reflected', color='blue')
    plt.plot(data['H'], data['Absorbed']/1000, label='Absorbed', color='orange')
    plt.plot(data['H'], data['Transmitted']/1000, label='Transmitted', color='grey')

    # Adding titles and labels
    plt.title('Fraction of Neutrons Reflected/Absorbed/Transmitted Through material of thickness H')
    plt.xlabel('H (thickness of material)')
    plt.ylabel('Fraction of Neutrons (n = 1000)')
    
    # Adding a legend
    plt.legend()
    
    # Adjust layout to make room for plots and remove extra white space
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    # Saving the plot to a PNG file
    plt.savefig('neutron_interaction_plot.png')

    plt.show()

# Usage
csv_file_path = 'data_for_paper/sweep_data.csv'  
plot_neutron_data(csv_file_path)
