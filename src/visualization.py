"""Warehouse analytics visualization."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class WarehouseVisualizer:
    def __init__(self, output_dir="data/"):
        self.output_dir = output_dir

    def plot_sales_trend(self, df, x_col, y_col, title="Sales Trend", save=True):
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df[x_col], df[y_col], marker="o", color="steelblue")
        ax.set_title(title)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        if save:
            fig.savefig(f"{self.output_dir}sales_trend.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
