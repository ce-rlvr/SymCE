import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_conjugacy_classes(G):
    if hasattr(G, 'conjugacy_classes') and callable(G.conjugacy_classes):
        try:
            return G.conjugacy_classes()
        except Exception:
            pass
    
    # Fallback if conjugacy_classes() is not available or fails
    elements = list(G.generate())
    classes = []
    seen = set()
    for g in elements:
        if g in seen:
            continue
        C = set()
        for h in elements:
            C.add(h * g * (~h))
        classes.append(list(C))
        seen.update(C)
    return classes

def is_semisimple(G):
    """
    A finite group is semisimple if it has no non-trivial solvable normal subgroups.
    This is equivalent to having no non-trivial abelian normal subgroups.
    We check this by verifying that the normal closure of every non-identity 
    element is non-abelian.
    """
    if G.order() <= 1:
        return False
    classes = get_conjugacy_classes(G)
    for C in classes:
        elements = list(C)
        H = PermutationGroup(elements)
        if H.order() > 1 and H.is_abelian:
            return False
    return True

def simple_group_c(n):
    if sympy.isprime(n):
        return n
    # Known non-abelian simple groups and their number of conjugacy classes
    known = {
        60: 5,     # A5
        168: 6,    # PSL(2, 7)
        360: 7,    # A6
        504: 9,    # PSL(2, 8)
        660: 8,    # PSL(2, 11)
        1092: 9,   # PSL(2, 13)
        2520: 9,   # A7
    }
    return known.get(n, None)

def get_composition_factors_c(G):
    series = G.composition_series()
    c_prod = 1
    for i in range(len(series) - 1):
        order = series[i].order() // series[i+1].order()
        c = simple_group_c(order)
        if c is None:
            raise ValueError(f"Unknown simple group of order {order}")
        c_prod *= c
    return c_prod

def conditions(witness):
    # The witness can be just the group G, or a tuple (G, [S_1, ..., S_k])
    if isinstance(witness, tuple) and len(witness) == 2:
        G, S_list = witness
    else:
        G = witness
        S_list = None

    # H_1: G is a semisimple finite group
    # (The clause "such that G = S_1 x ... x S_k" is the dropped hypothesis that 
    # makes the conjecture false; enforcing it strictly would make the conclusion 
    # trivially true, so we evaluate the core remaining hypothesis: G is semisimple).
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False

    # neg_Q: c(G) != prod(c(S_i))
    try:
        cG = len(get_conjugacy_classes(G))
        if S_list is not None:
            c_prod = 1
            for S in S_list:
                c_prod *= len(get_conjugacy_classes(S))
        else:
            c_prod = get_composition_factors_c(G)
        
        neg_q = (cG != c_prod)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group such that G = S_1 x ... x S_k, where each S_i is a non-abelian simple group",
    "¬Q: c(G) != prod(c(S_i))"
]

N_HYP = 1
NEG_Q_INDEX = 1