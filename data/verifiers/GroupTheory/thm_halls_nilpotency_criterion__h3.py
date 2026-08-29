import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_nilpotent_quotient(G, N):
    current = G
    try:
        G_elems = list(G.elements)
    except Exception:
        G_elems = list(G.generate())
        
    while True:
        if current.is_subgroup(N):
            return True
            
        try:
            current_elems = list(current.elements)
        except Exception:
            current_elems = list(current.generate())
            
        commutators = set()
        for g in G_elems:
            for c in current_elems:
                commutators.add(g**-1 * c**-1 * g * c)
                
        if not commutators:
            next_group = PermutationGroup([G.identity])
        else:
            next_group = PermutationGroup(list(commutators))
            
        if next_group.order() == current.order():
            return False
        current = next_group

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    try:
        NN = N.derived_subgroup()
        h3 = is_nilpotent_quotient(G, NN)
    except Exception:
        h3 = False

    try:
        if callable(G.is_nilpotent):
            neg_q = not G.is_nilpotent()
        else:
            neg_q = not G.is_nilpotent
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: The quotient group G/derived(N) is nilpotent",
    "¬Q: G is not nilpotent"
]

N_HYP = 3
NEG_Q_INDEX = 3