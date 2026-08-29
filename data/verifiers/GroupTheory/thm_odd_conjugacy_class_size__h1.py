import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, x), checks if it is a valid counterexample to the conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        G, x = witness
    except Exception:
        return [False, False]
    
    # H_1: Let x be an element of G.
    try:
        if hasattr(G, 'contains'):
            if callable(G.contains):
                h1 = bool(G.contains(x))
            else:
                h1 = bool(x in G)
        elif hasattr(G, '__contains__'):
            h1 = bool(x in G)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The size of the conjugacy class of x in G is odd iff C_G(x) contains a Sylow 2-subgroup of G.
    # We evaluate the equivalence and negate it.
    try:
        # 1. Check if conjugacy class size is odd
        if hasattr(G, 'conjugacy_class_size_is_odd'):
            if callable(G.conjugacy_class_size_is_odd):
                is_odd = bool(G.conjugacy_class_size_is_odd(x))
            else:
                is_odd = bool(G.conjugacy_class_size_is_odd)
        elif hasattr(G, 'conjugacy_class_size'):
            if callable(G.conjugacy_class_size):
                c_size = G.conjugacy_class_size(x)
            else:
                c_size = G.conjugacy_class_size
            try:
                is_odd = (int(c_size) % 2 == 1)
            except Exception:
                is_odd = False
        else:
            # Fallback for standard SymPy PermutationGroup
            order_G = G.order()
            order_C = G.centralizer(x).order()
            try:
                c_size = int(order_G) // int(order_C)
                is_odd = (c_size % 2 == 1)
            except Exception:
                is_odd = False
            
        # 2. Check if C_G(x) contains a Sylow 2-subgroup of G
        if hasattr(G, 'centralizer_contains_sylow_2'):
            if callable(G.centralizer_contains_sylow_2):
                contains_sylow = bool(G.centralizer_contains_sylow_2(x))
            else:
                contains_sylow = bool(G.centralizer_contains_sylow_2)
        else:
            # Fallback for standard SymPy PermutationGroup
            C = G.centralizer(x)
            s_G = G.sylow_subgroup(2).order()
            s_C = C.sylow_subgroup(2).order()
            # C_G(x) contains a Sylow 2-subgroup of G iff its own Sylow 2-subgroup 
            # has the same order as the Sylow 2-subgroup of G.
            contains_sylow = (int(s_C) == int(s_G))
            
        # The conclusion is the equivalence of the two properties
        conclusion = (is_odd == contains_sylow)
        
        # We want the conclusion to FAIL at the witness
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: The equivalence (conjugacy class size is odd iff C_G(x) contains a Sylow 2-subgroup of G) FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1