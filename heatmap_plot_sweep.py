import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmaps(csv_file_path):
    # Load the data
    data = pd.read_csv(csv_file_path)

    # Creating pivot tables for each parameter
    transmitted_pivot = data.pivot(index="A", columns="H", values="Transmitted") / 1000  # Divided by 1000 if values are counts
    absorbed_pivot = data.pivot(index="A", columns="H", values="Absorbed") / 1000
    reflected_pivot = data.pivot(index="A", columns="H", values="Reflected") / 1000

    # Plotting heatmaps
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Transmitted heatmap
    sns.heatmap(transmitted_pivot, ax=axs[0], cmap="viridis")
    axs[0].set_title("Transmitted Fraction")
    axs[0].set_xlabel("H (material thickness)")
    axs[0].set_ylabel("A (absorption coefficient)")

    # Absorbed heatmap
    sns.heatmap(absorbed_pivot, ax=axs[1], cmap="magma")
    axs[1].set_title("Absorbed Fraction")
    axs[1].set_xlabel("H (material thickness)")
    axs[1].set_ylabel("A (absorption coefficient)")

    # Reflected heatmap
    sns.heatmap(reflected_pivot, ax=axs[2], cmap="coolwarm")
    axs[2].set_title("Reflected Fraction")
    axs[2].set_xlabel("H (material thickness)")
    axs[2].set_ylabel("A (absorption coefficient)")

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig("neutron_heatmaps.png")
    plt.show()

    


# Usage
csv_file_path = 'data_for_paper/sweep_data.csv'  
plot_heatmaps(csv_file_path)
