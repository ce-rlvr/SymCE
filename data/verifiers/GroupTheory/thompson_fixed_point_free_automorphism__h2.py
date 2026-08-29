import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics import PermutationGroup, Permutation
from sympy import isprime

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

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        G, alpha = witness
    except Exception:
        return [False, False, False, False]

    def apply_alpha(x):
        if isinstance(alpha, dict):
            return alpha[x]
        else:
            return alpha(x)

    # H1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H2: alpha(x) = x implies x = e for all x in G
    try:
        h2_ok = True
        if not h1_ok:
            h2_ok = False
        else:
            elements = list(G.generate())
            elem_set = set(elements)
            
            # Check if alpha is a well-defined map from G to G
            for x in elements:
                ax = apply_alpha(x)
                if ax not in elem_set:
                    h2_ok = False
                    break
            
            if h2_ok:
                # Check if alpha is a bijection
                image = set(apply_alpha(x) for x in elements)
                if len(image) != len(elements):
                    h2_ok = False
            
            if h2_ok:
                # Find the identity element
                ident = None
                for x in elements:
                    if x * x == x:
                        ident = x
                        break
                
                # Check the fixed-point-free condition
                for x in elements:
                    if apply_alpha(x) == x and x != ident:
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False

    # H3: The order of alpha is a prime number
    try:
        h3_ok = False
        if h1_ok and h2_ok:
            elements = list(G.generate())
            elem_to_idx = {elem: i for i, elem in enumerate(elements)}
            perm_array = [elem_to_idx[apply_alpha(elem)] for elem in elements]
            p = Permutation(perm_array)
            order = p.order() if callable(getattr(p, 'order', None)) else p.order
            h3_ok = isprime(order)
    except Exception:
        h3_ok = False

    # neg_Q: G is not a nilpotent group
    try:
        neg_q_ok = False
        if h1_ok:
            if callable(getattr(G, 'is_nilpotent', None)):
                neg_q_ok = not G.is_nilpotent()
            else:
                neg_q_ok = not G.is_nilpotent
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: alpha(x) = x implies x = e for all x in G",
    "H_3: The order of alpha is a prime number",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 3
NEG_Q_INDEX = 3