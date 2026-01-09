import numpy as np
from sklearn.neighbors import NearestNeighbors
from config import (
    SITE_W, SITE_H, BUFFER, MIN_SEP,
    PLAZA, NEIGHBOR_LIMIT
)

def check_constraints(x, y, w, h, placed_buildings):
    """
    Checks boundary, buffer, plaza overlap,
    and minimum separation constraints.
    """
    # Boundary & buffer check
    if (
        x < BUFFER or y < BUFFER or
        x + w > SITE_W - BUFFER or
        y + h > SITE_H - BUFFER
    ):
        return False

    # Central plaza check
    px, py, pw, ph = PLAZA
    if not (
        x + w < px or x > px + pw or
        y + h < py or y > py + ph
    ):
        return False

    # Minimum separation check
    for bx, by, bw, bh, _ in placed_buildings:
        if not (
            x + w + MIN_SEP <= bx or
            x >= bx + bw + MIN_SEP or
            y + h + MIN_SEP <= by or
            y >= by + bh + MIN_SEP
        ):
            return False

    return True


def validate_neighbor_rule(buildings):
    """
    Ensures every Tower A has at least one Tower B
    within NEIGHBOR_LIMIT distance.
    """
    towers_a = [
        np.array([b[0] + b[2] / 2, b[1] + b[3] / 2])
        for b in buildings if b[4] == 'A'
    ]
    towers_b = [
        np.array([b[0] + b[2] / 2, b[1] + b[3] / 2])
        for b in buildings if b[4] == 'B'
    ]

    if not towers_a or not towers_b:
        return False

    nn = NearestNeighbors(radius=NEIGHBOR_LIMIT)
    nn.fit(towers_b)

    for a_center in towers_a:
        neighbors = nn.radius_neighbors([a_center])[0][0]
        if len(neighbors) == 0:
            return False

    return True
