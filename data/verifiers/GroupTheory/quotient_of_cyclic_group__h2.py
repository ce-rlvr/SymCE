import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a cyclic group
    try:
        h1 = False
        if hasattr(G, 'is_cyclic'):
            h1_attr = G.is_cyclic
            if callable(h1_attr):
                h1 = bool(h1_attr())
            else:
                h1 = bool(h1_attr)
    except Exception:
        h1 = False
        
    # ¬Q: The subgroup N is normal in G, and the quotient group G/N is cyclic (must FAIL)
    try:
        q = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            # Check if N is a subgroup of G
            is_sub = all(G.contains(gen) for gen in N.generators)
            if is_sub:
                # Check if N is normal in G
                is_normal = True
                for h in N.generators:
                    for g in list(G.generate()):
                        if not N.contains(g * h * ~g):
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                if is_normal:
                    g_order = G.order() if callable(getattr(G, 'order', None)) else G.order
                    n_order = N.order() if callable(getattr(N, 'order', None)) else N.order
                    order_quotient = g_order // n_order
                    
                    # Check if G/N is cyclic
                    is_cyclic_quotient = False
                    for g in list(G.generate()):
                        k = 1
                        curr = g
                        while not N.contains(curr) and k <= order_quotient:
                            curr = curr * g
                            k += 1
                        if k == order_quotient and N.contains(curr):
                            is_cyclic_quotient = True
                            break
                    q = is_cyclic_quotient
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: N is not a normal subgroup of G, or G/N is not cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1