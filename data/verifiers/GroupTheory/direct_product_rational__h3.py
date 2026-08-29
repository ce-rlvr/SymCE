import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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

def is_rational_group(G):
    try:
        elements = list(G.elements)
    except AttributeError:
        return False
    
    classes = []
    seen = set()
    for g in elements:
        if g not in seen:
            # Compute the conjugacy class of g
            c = {x * g * ~x for x in elements}
            classes.append(c)
            seen.update(c)
            
    for c in classes:
        g = next(iter(c))
        try:
            m = g.order()
        except TypeError:
            m = g.order
            
        for k in range(1, m):
            if math.gcd(k, m) == 1:
                if g**k not in c:
                    return False
    return True

def direct_product(G, H):
    m = G.degree
    n = H.degree
    gens = []
    
    for g in G.generators:
        p = list(g.array_form)
        if len(p) < m:
            p += list(range(len(p), m))
        p += list(range(m, m + n))
        gens.append(Permutation(p))
        
    for h in H.generators:
        p = list(h.array_form)
        if len(p) < n:
            p += list(range(len(p), n))
        p = list(range(m)) + [x + m for x in p]
        gens.append(Permutation(p))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are finite groups
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: G is a rational group
    try:
        h2_ok = is_rational_group(G)
    except Exception:
        h2_ok = False
        
    # neg_Q: G x H is NOT a rational group
    try:
        GxH = direct_product(G, H)
        neg_q_ok = not is_rational_group(GxH)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: G is a rational group",
    "¬Q: G x H is not a rational group"
]

N_HYP = 2
NEG_Q_INDEX = 2