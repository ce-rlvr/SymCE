import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])

def _order(obj):
    return obj.order() if callable(obj.order) else obj.order

def _elements(group):
    els = group.elements
    return els() if callable(els) else els

def _generators(group):
    gens = group.generators
    return gens() if callable(gens) else gens

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group and N is a normal subgroup of G
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            h1 = False
        else:
            gens_N = _generators(N)
            gens_G = _generators(G)
            is_sub = all(G.contains(n) for n in gens_N)
            if not is_sub:
                h1 = False
            else:
                h1 = all(N.contains(g * n * ~g) for n in gens_N for g in gens_G)
    except Exception:
        h1 = False

    # H2: N is a cyclic group
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            n_order = _order(N)
            h2 = any(_order(n) == n_order for n in _elements(N))
    except Exception:
        h2 = False

    # H3: The quotient group G/N is a cyclic group
    try:
        if not h1:
            h3 = False
        else:
            index = _order(G) // _order(N)
            h3 = False
            for g in _elements(G):
                k = 1
                while k <= index:
                    if N.contains(g**k):
                        break
                    k += 1
                if k == index:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup G' is NOT a cyclic group
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            C = G.derived_subgroup()
            c_order = _order(C)
            is_cyclic = any(_order(c) == c_order for c in _elements(C))
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N is a normal subgroup of G",
    "H_2: N is a cyclic group",
    "H_3: The quotient group G/N is a cyclic group",
    "¬Q: The commutator subgroup G' is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3