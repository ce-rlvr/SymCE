import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation(0, 1) * Permutation(2, 3),
    Permutation(0, 2) * Permutation(1, 3)
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_rational_group(grp):
    """
    A group is rational if all its irreducible complex characters are rational-valued.
    This is equivalent to: for every g in G, and every k coprime to the order of g,
    g^k is conjugate to g in G.
    """
    try:
        if not hasattr(grp, 'elements'):
            return False
        elements = list(grp.elements)
        
        # Precompute conjugacy classes to speed up the check
        conjugacy_classes = []
        seen = set()
        for g in elements:
            if g in seen:
                continue
            orbit = set()
            for x in elements:
                orbit.add(x * g * ~x)
            conjugacy_classes.append(orbit)
            seen.update(orbit)
            
        for orbit in conjugacy_classes:
            g = next(iter(orbit))
            order = g.order()
            for k in range(1, order):
                if math.gcd(k, order) == 1:
                    gk = g**k
                    if gk not in orbit:
                        return False
        return True
    except Exception:
        return False

def direct_product(G, H):
    """
    Constructs the direct product of two permutation groups G and H.
    """
    m = G.degree
    n = H.degree
    gens = []
    
    for g in G.generators:
        arr = list(g.array_form)
        if len(arr) < m:
            arr += list(range(len(arr), m))
        arr += list(range(m, m + n))
        gens.append(Permutation(arr))
        
    for h in H.generators:
        arr = list(range(m))
        h_arr = list(h.array_form)
        if len(h_arr) < n:
            h_arr += list(range(len(h_arr), n))
        arr += [x + m for x in h_arr]
        gens.append(Permutation(arr))
        
    if not gens:
        gens.append(Permutation(m + n - 1))
        
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_rational_group(G)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_rational_group(H)
    except Exception:
        h2_ok = False
        
    try:
        DP = direct_product(G, H)
        neg_q_ok = not is_rational_group(DP)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a rational group",
    "H_2: H is a rational group",
    "¬Q: The direct product G \\times H is not a rational group"
]

N_HYP = 2
NEG_Q_INDEX = 2