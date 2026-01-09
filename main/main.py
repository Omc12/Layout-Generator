from generator import generate_one_layout
from visualize import plot_layouts

def main():
    print("Finding 4 best layouts...")
    valid_layouts = []

    while len(valid_layouts) < 4:
        result = generate_one_layout()
        if result:
            valid_layouts.append(result)

    plot_layouts(valid_layouts)

if __name__ == "__main__":
    main()
