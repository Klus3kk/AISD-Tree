import matplotlib.pyplot as plt
import numpy as np
import os

def smooth_data(y, window_size):
    """ Smooth data using a moving average with minimal boundary distortion. """
    if window_size < 2:
        return y
    window = np.ones(int(window_size)) / float(window_size)
    y_padded = np.pad(y, pad_width=(window_size//2, window_size//2), mode='edge')
    return np.convolve(y_padded, window, 'same')[window_size//2:-window_size//2+1]

def sanitize_filename(filename):
    """ Sanitize the filename by replacing or removing invalid characters. """
    return filename.replace(' ', '_').replace('/', '_or_')

def load_and_plot(filename):
    # Load data
    results = np.loadtxt(filename, delimiter=",", skiprows=1)

    # Unpack data accurately according to your column description
    sizes = results[:, 0]
    bst_creation_times = results[:, 1]
    avl_creation_times = results[:, 2]
    bst_min_max_times = results[:, 3]
    avl_min_max_times = results[:, 4]
    bst_in_order_times = results[:, 5]
    avl_in_order_times = results[:, 6]
    rebalance_times = results[:, 7]

    # Apply smoothing
    smoothed_bst_creation = smooth_data(bst_creation_times, 5)
    smoothed_avl_creation = smooth_data(avl_creation_times, 5)
    smoothed_bst_min_max = smooth_data(bst_min_max_times, 5)
    smoothed_avl_min_max = smooth_data(avl_min_max_times, 5)
    smoothed_bst_in_order = smooth_data(bst_in_order_times, 5)
    smoothed_avl_in_order = smooth_data(avl_in_order_times, 5)
    smoothed_rebalance = smooth_data(rebalance_times, 5)

    # Base filename without extension
    base_filename = os.path.splitext(os.path.basename(filename))[0]

    def plot_times(sizes, times, title, ylabel, log_scale=False):
        plt.figure(figsize=(10, 5))
        plt.plot(sizes, times, linestyle='-', color='blue', label='BST')
        if log_scale:
            plt.yscale('log')
        plt.title(title)
        plt.xlabel('Number of Elements in Tree')
        plt.ylabel(ylabel)
        plt.grid(True, which="both", ls="--")
        plt.legend()
        plt.savefig(f"{base_filename}_{sanitize_filename(title)}.png")
        plt.show()

    # Plot function
    def plot_comparison(sizes, data1, data2, title, ylabel, log_scale=False):
        plt.figure(figsize=(10, 5))
        plt.plot(sizes, data1, linestyle='-', color='blue', label='BST')
        plt.plot(sizes, data2, linestyle='-', color='red', label='AVL')
        if log_scale:
            plt.yscale('log')
        plt.title(title)
        plt.xlabel('Number of Elements in Tree')
        plt.ylabel(ylabel)
        plt.grid(True, which="both", ls="--")
        plt.legend()
        plt.savefig(f"{base_filename}_{sanitize_filename(title)}.png")
        plt.show()


    # Generating the plots
    plot_comparison(sizes, smoothed_bst_creation, smoothed_avl_creation, "Creation Time Comparison", "Time (s)")
    plot_comparison(sizes, smoothed_bst_min_max, smoothed_avl_min_max, "Find Min/Max Time Comparison", "Time (s)")
    plot_comparison(sizes, smoothed_bst_in_order, smoothed_avl_in_order, "In-Order Traversal Time Comparison", "Time (s)")
    plot_times(sizes, smoothed_rebalance, "Rebalancing BST Time", "Time (s)")

# List of filenames
filenames = ["benchmark_results_constant.csv", "benchmark_results_random.csv", 
             "benchmark_results_a_shaped.csv", "benchmark_results_decreasing.csv", 
             "benchmark_results_increasing.csv"]

# Generate graphs for all files
for file in filenames:
    load_and_plot(file)

    
