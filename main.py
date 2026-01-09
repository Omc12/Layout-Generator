import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from sklearn.neighbors import NearestNeighbors
import random

SITE_W, SITE_H = 200, 140
BUFFER = 10
MIN_SEP = 15
PLAZA = (80, 50, 40, 40) # x, y, w, h
NEIGHBOR_LIMIT = 60
TOWER_SIZES = {'A': (30, 20), 'B': (20, 20)}

# Checks if a building at (x,y) with size (w,h) is legal.

def check_constraints(x, y, w, h, placed_buildings):
    # Boundry & 10m Buffer check
    if x < BUFFER or y < BUFFER or x + w > SITE_W - BUFFER or y + h > SITE_H - BUFFER:
        return False
    
    #Central plaza check
    px, py, pw, ph = PLAZA
    if not(x + w < px or x > px + pw or y + h < py or y > py + ph):
        return False
    
    #15m separation check
    for (bx, by, bw,bh, _) in placed_buildings:
        if not (x + w + MIN_SEP <= bx or x >= bx + bw + MIN_SEP or
                y + h + MIN_SEP <= by or y >= by + bh + MIN_SEP):
            return False
    return True

 #Ensures every Tower A has a Tower B within 60m.
def validate_neighbor_rule(buildings):
    towers_a = [np.array([b[0]+b[2]/2, b[1]+b[3]/2]) for b in buildings if b[4] == 'A']
    towers_b = [np.array([b[0]+b[2]/2, b[1]+b[3]/2]) for b in buildings if b[4] == 'B']

    if not towers_a: return False
    if not towers_b: return False

    nn = NearestNeighbors(radius=NEIGHBOR_LIMIT)
    nn.fit(towers_b)
    for a_center in towers_a:
        if len(nn.radius_neighbors([a_center])[0][0]) == 0:
            return False
    return True

# Generates a single valid layout by trying random placements.
def generate_one_layout():
    buildings = []

    # FIRST: Force at least 3 Tower As to be present
    for _ in range(20):
        w, h = TOWER_SIZES['A']
        rx, ry = random.uniform(0, SITE_W), random.uniform(0, SITE_H)
        if check_constraints(rx, ry, w, h, buildings):
            buildings.append((rx, ry, w, h, 'A'))
            if len([b for b in buildings if b[4] == 'A']) >= 3: break

    # SECOND: Fill the rest of the site with A or B
    for _ in range(150):
        b_type = random.choice(['A', 'B'])
        w, h = TOWER_SIZES[b_type]
        rx, ry = random.uniform(0, SITE_W), random.uniform(0, SITE_H)
        if check_constraints(rx, ry, w, h, buildings):
            buildings.append((rx, ry, w, h, b_type))

    # Validate final neighbor rule
    if validate_neighbor_rule(buildings) and len(buildings) >= 6:
        area = sum([b[2] * b[3] for b in buildings])
        return {'layout': buildings, 'area': area}
    return None

# --- MAIN EXECUTION ---
print("Finding 4 best layouts...")
valid_layouts = []
while len(valid_layouts) < 4:
    res = generate_one_layout()
    if res:
        valid_layouts.append(res)

# Visualize the 4 results
fig, axes = plt.subplots(2, 2, figsize = (14, 10))
axes = axes.flatten()

for i, res in enumerate(valid_layouts):
    ax =axes[i]
     # Draw Site boundary and Plaza
    ax.add_patch(patches.Rectangle((0, 0), SITE_W, SITE_H, fill=False, edgecolor = 'black', lw=2))
    ax.add_patch(patches.Rectangle((80, 50), 40, 40, color='red', alpha=0.2, hatch='////'))

    for (x, y, w, h, b_type) in res['layout']:
        color = 'dodgerblue' if b_type == 'A' else 'limegreen'
        ax.add_patch(patches.Rectangle((x, y), w, h, color=color, ec='black', alpha=0.8))
        ax.text(x+w/2, y+h/2, b_type, ha='center', va='center', color='white', weight='bold')

    ax.set_title(f"Layout {i+1} | Area:{res['area']}m²")
    ax.set_xlim(-10, 210); ax.set_ylim(-10, 150); ax.set_aspect('equal')

plt.tight_layout()
plt.savefig("layouts.png", dpi=300, bbox_inches="tight")
plt.show()