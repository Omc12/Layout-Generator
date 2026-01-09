import random
from config import SITE_W, SITE_H, TOWER_SIZES
from constraints import check_constraints, validate_neighbor_rule

def generate_one_layout():
    """
    Generates a single valid site layout using random sampling.
    """
    buildings = []

    # Ensure at least 3 Tower A
    for _ in range(20):
        w, h = TOWER_SIZES['A']
        x = random.uniform(0, SITE_W)
        y = random.uniform(0, SITE_H)

        if check_constraints(x, y, w, h, buildings):
            buildings.append((x, y, w, h, 'A'))

        if len([b for b in buildings if b[4] == 'A']) >= 3:
            break

    # Fill remaining site
    for _ in range(150):
        b_type = random.choice(['A', 'B'])
        w, h = TOWER_SIZES[b_type]
        x = random.uniform(0, SITE_W)
        y = random.uniform(0, SITE_H)

        if check_constraints(x, y, w, h, buildings):
            buildings.append((x, y, w, h, b_type))

    # Final validation
    if validate_neighbor_rule(buildings) and len(buildings) >= 6:
        total_area = sum(b[2] * b[3] for b in buildings)
        return {
            "layout": buildings,
            "area": total_area
        }

    return None
