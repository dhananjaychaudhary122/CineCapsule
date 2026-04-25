import os
import matplotlib.pyplot as plt
import seaborn as sns

def setup_directories():
    """Ensure all required directories exist."""
    dirs = ['data', 'models', 'outputs', 'reports']
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    print(f"Directories checked in {base_dir}")

def save_plot(fig, filename):
    """Save a matplotlib figure to the outputs directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    path = os.path.join(output_dir, filename)
    fig.savefig(path)
    print(f"Saved plot to {path}")

def set_plot_style():
    """Set the aesthetic style of the plots."""
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
