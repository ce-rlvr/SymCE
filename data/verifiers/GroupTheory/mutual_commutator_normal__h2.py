import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(N, G):
    try:
        return all(G.contains(g) for g in N.generators)
    except Exception:
        return False

def is_normal_subgroup(H, G):
    try:
        if not is_subgroup(H, G):
            return False
        for h in H.generators:
            for g in G.generators:
                if not H.contains((~g) * h * g):
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group (and N is a subgroup of G)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and is_subgroup(N, G)
    except Exception:
        h1 = False
        
    # neg_Q: The mutual commutator subgroup of N and G is not a normal subgroup of G
    try:
        if not h1:
            neg_q = False
        elif G.order() * N.order() > 200000:
            # Prevent timeouts for excessively large groups
            neg_q = False
        else:
            gens = set()
            for n in N.generate():
                for g in G.generate():
                    c = (~n) * (~g) * n * g
                    if c not in gens:
                        gens.add(c)
            
            NG_comm = PermutationGroup(list(gens))
            neg_q = not is_normal_subgroup(NG_comm, G)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The mutual commutator subgroup of N and G is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1