import matplotlib.pyplot as plt
import matplotlib.patches as patches
from config import SITE_W, SITE_H, PLAZA

def plot_layouts(layouts, filename="layouts.png"):
    """
    Visualizes multiple layouts in a 2x2 grid.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for i, result in enumerate(layouts):
        ax = axes[i]

        # Site boundary
        ax.add_patch(
            patches.Rectangle(
                (0, 0), SITE_W, SITE_H,
                fill=False, edgecolor='black', lw=2
            )
        )

        # Central plaza
        px, py, pw, ph = PLAZA
        ax.add_patch(
            patches.Rectangle(
                (px, py), pw, ph,
                color='red', alpha=0.2, hatch='////'
            )
        )

        # Buildings
        for x, y, w, h, b_type in result["layout"]:
            color = 'dodgerblue' if b_type == 'A' else 'limegreen'
            ax.add_patch(
                patches.Rectangle(
                    (x, y), w, h,
                    color=color, ec='black', alpha=0.8
                )
            )
            ax.text(
                x + w / 2, y + h / 2, b_type,
                ha='center', va='center',
                color='white', weight='bold'
            )

        ax.set_title(f"Layout {i + 1} | Area: {result['area']} m²")
        ax.set_xlim(-10, SITE_W + 10)
        ax.set_ylim(-10, SITE_H + 10)
        ax.set_aspect('equal')

    plt.tight_layout()
    plt.show()
