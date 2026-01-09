import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

def generate_layout():
    # Site Constants
    SITE_W, SITE_H = 200, 140
    BUFFER = 10
    PLAZA = (80, 50, 40, 40) # x, y, w, h
    SEP = 15

    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 1. Draw Site & Buffer
    ax.set_xlim(-10, 210)
    ax.set_ylim(-10, 150)
    ax.add_patch(patches.Rectangle((0, 0), SITE_W, SITE_H, fill=False, edgecolor='black', lw=2, ls='--'))
    ax.add_patch(patches.Rectangle((0, 0), SITE_W, SITE_H, color='red', alpha=0.1, label='10m Boundary Buffer'))
    ax.add_patch(patches.Rectangle((BUFFER, BUFFER), SITE_W-2*BUFFER, SITE_H-2*BUFFER, color='white'))

    # 2. Draw Plaza
    ax.add_patch(patches.Rectangle((PLAZA[0], PLAZA[1]), PLAZA[2], PLAZA[3], color='red', alpha=0.3, label='Central Plaza'))

    # 3. Simple Placement Logic (Mocking the Generator)
    buildings = [
        {'type': 'A', 'pos': (20, 20), 'size': (30, 20)},
        {'type': 'B', 'pos': (60, 20), 'size': (20, 20)},
        {'type': 'A', 'pos': (150, 20), 'size': (30, 20)},
        {'type': 'B', 'pos': (150, 60), 'size': (20, 20)},
        {'type': 'A', 'pos': (20, 100), 'size': (30, 20)},
        {'type': 'B', 'pos': (70, 100), 'size': (20, 20)},
        {'type': 'B', 'pos': (120, 100), 'size': (20, 20)},
        {'type': 'A', 'pos': (160, 100), 'size': (30, 20)},
    ]

    for b in buildings:
        color = 'royalblue' if b['type'] == 'A' else 'seagreen'
        ax.add_patch(patches.Rectangle(b['pos'], b['size'][0], b['size'][1], color=color, edgecolor='black', alpha=0.8))
        ax.text(b['pos'][0]+2, b['pos'][1]+2, b['type'], color='white', fontweight='bold')

    plt.title("Automated Layout Generation: Example Configuration")
    plt.legend(loc='upper right', fontsize='small')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

generate_layout()