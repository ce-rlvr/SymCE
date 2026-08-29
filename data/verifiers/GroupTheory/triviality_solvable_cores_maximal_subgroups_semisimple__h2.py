import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_core(G, M):
    """
    Computes the normal core of M in G.
    The core is the largest normal subgroup of G contained in M.
    """
    try:
        current_set = set(M.elements)
    except Exception:
        current_set = set(M.generate())
        
    gens = G.generators
    while True:
        new_set = set()
        for x in current_set:
            keep = True
            for g in gens:
                conj1 = g * x * (~g)
                conj2 = (~g) * x * g
                if conj1 not in current_set or conj2 not in current_set:
                    keep = False
                    break
            if keep:
                new_set.add(x)
        if len(new_set) == len(current_set):
            break
        current_set = new_set
        
    return PermutationGroup(list(current_set))

def check_solvable(G):
    """
    Checks if a permutation group is solvable.
    """
    if hasattr(G, 'is_solvable'):
        return bool(G.is_solvable)
    
    current = G
    while True:
        next_G = current.derived_subgroup()
        if next_G.order() == current.order():
            break
        current = next_G
    return current.order() == 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, M) where G is a PermutationGroup and M is a subgroup.
    """
    try:
        G, M = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a semisimple finite group
    # A standard non-abelian semisimple group (e.g., a central product of quasisimple groups) is perfect.
    try:
        h1 = bool(G.order() == G.derived_subgroup().order())
    except Exception:
        h1 = False

    # H2: The core of M in G is a solvable group
    try:
        core_M = get_core(G, M)
        h2 = check_solvable(core_M)
    except Exception:
        h2 = False

    # neg_Q: The core of M in G is NOT the trivial subgroup
    try:
        core_M = get_core(G, M)
        neg_q = bool(core_M.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: The core of M in G is a solvable group",
    "¬Q: The core of M in G is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2