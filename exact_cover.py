import sys
import subprocess
import shutil
from argparse import ArgumentParser
from itertools import combinations

def load_instance(input_file_name):
    # read the input instance
    # the instance consists of a universe of elements and a list of subsets
    # we need to select subsets such that every element appears exactly once
    global UNIVERSE, SUBSETS, SUBSET_NAMES, NR_VARS
    with open(input_file_name, "r") as file:
        lines = [l.strip() for l in file if l.strip()]
    if not lines:
        print("Error: Empty file")
        sys.exit(1)

    # Parse universe
    if lines[0].startswith("Universe:"):
        UNIVERSE = set(lines[0].replace("Universe:", "").strip().split())
    else:
        UNIVERSE = set(lines[0].split())

    SUBSETS = []
    SUBSET_NAMES = []

    # Parse subsets
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        s_name = parts[0].strip(':')
        s_elements = parts[1:]
        valid_elements = [e for e in s_elements if e in UNIVERSE]
        if valid_elements:
            SUBSET_NAMES.append(s_name)
            SUBSETS.append(set(valid_elements))

    NR_VARS = len(SUBSETS)
    return SUBSETS

def encode(subsets):
    # given the instance, create a cnf formula
    # variables encode which subset is selected
    # variables are numbered from 1 to N - number of subsets
    
    cnf = []
    element_to_vars = {e: [] for e in UNIVERSE}
    for i, subset in enumerate(subsets):
        var_id = i + 1
        for elem in subset:
            if elem in element_to_vars:
                element_to_vars[elem].append(var_id)

    # At least one subset must cover each element
    # For each element e, add clause S_i v S_j v... where e is in S_i, S_j...
    for element, _vars in element_to_vars.items():
        if not _vars:
            # If an element is not in any subset, the problem is unsolvable
            cnf.append([1, 0])
            cnf.append([-1, 0])
            return cnf, NR_VARS
        clause = _vars[:]
        clause.append(0)
        cnf.append(clause)

    # Ensure no two selected subsets share an element
    # For each element e, if e is in S_i and S_j, add clause -S_i v -S_j
    for element, _vars in element_to_vars.items():
        for i, j in combinations(_vars, 2):
            cnf.append([-i, -j, 0])

    return (cnf, NR_VARS)

def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    # print CNF into formula.cnf in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    # call the solver and return the output
    cmd = [solver_name, '-model', '-verb=' + str(verbosity), output_name]
    
    if "/" not in solver_name and not shutil.which(solver_name):
         cmd[0] = "./" + solver_name
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print(f"Error: Solver '{solver_name}' not found.")
        sys.exit(1)

def print_result(result):
    if result.stdout:
        for line in result.stdout.decode('utf-8').split('\n'):
            print(line)
    
    if (result.returncode == 20):
        print("Result: UNSATISFIABLE")
        return

    # parse the model from the output of the solver
    model = []
    if result.stdout:
        for line in result.stdout.decode('utf-8').split('\n'):
            if line.startswith("v"):
                vars = line.split(" ")
                vars.remove("v")
                for v in vars:
                    try:
                        val = int(v)
                        if val != 0:
                            model.append(val)
                    except ValueError:
                        pass
    
    print()
    print("##################################################################")
    print("###########[ Human readable result of Exact Cover ]###############")
    print("##################################################################")
    print()

    selected_subsets = []
    for val in model:
        if val > 0:
            idx = val - 1
            if idx < len(SUBSET_NAMES):
                selected_subsets.append(SUBSET_NAMES[idx])
    
    if not selected_subsets:
        print("No subsets selected (or parsing failed).")
    else:
        print("Subsets forming Exact Cover:")
        print(", ".join(selected_subsets))
        
        covered = []
        for name in selected_subsets:
            idx = SUBSET_NAMES.index(name)
            covered.extend(list(SUBSETS[idx]))
        
        print(f"\nTotal elements in universe: {len(UNIVERSE)}")
        print(f"Total elements covered:     {len(covered)}")
        print(f"Unique elements covered:    {len(set(covered))}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # get the input instance
    instance = load_instance(args.input)

    # encode the problem to create CNF formula
    cnf, nr_vars = encode(instance)

    # call the SAT solver and get the result
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)

    # interpret the result and print it in a human-readable format
    print_result(result)