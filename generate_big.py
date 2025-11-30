import random
import string

def generate_label(index):
    label = ""
    while index >= 0:
        label = chr(index % 26 + 65) + label
        index = index // 26 - 1
    return label

def generate_exact_cover(universe_size, num_extra_sets, max_set_size=5):
    # 1. Define Universe
    universe = list(range(1, universe_size + 1))
    
    # 2. Create the GUARANTEED SOLUTION (Partition the universe)
    # We shuffle the universe to ensure random grouping
    shuffled_universe = universe[:]
    random.shuffle(shuffled_universe)
    
    solution_sets = []
    while shuffled_universe:
        # Pick a random size for this subset
        size = random.randint(1, min(len(shuffled_universe), max_set_size))
        subset = sorted(shuffled_universe[:size])
        solution_sets.append(subset)
        shuffled_universe = shuffled_universe[size:]
        
    # 3. Create NOISE sets (Distractors)
    # These are random subsets that likely conflict with the solution
    noise_sets = []
    for _ in range(num_extra_sets):
        size = random.randint(1, max_set_size)
        subset = sorted(random.sample(universe, size))
        # Avoid duplicate sets
        if subset not in solution_sets and subset not in noise_sets:
            noise_sets.append(subset)
            
    # 4. Combine and Shuffle
    all_sets = solution_sets + noise_sets
    random.shuffle(all_sets)
    
    # 5. Output Formatting
    print(f"Universe: {' '.join(map(str, universe))}")
    
    for i, subset in enumerate(all_sets):
        label = generate_label(i)
        elements = " ".join(map(str, subset))
        print(f"{label}: {elements}")

# --- CONFIGURATION ---
# Change these numbers to make it bigger
UNIVERSE_SIZE = 20 
NUM_EXTRA_SETS = 15
MAX_SET_SIZE = 4

generate_exact_cover(UNIVERSE_SIZE, NUM_EXTRA_SETS, MAX_SET_SIZE)