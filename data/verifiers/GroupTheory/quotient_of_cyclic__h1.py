import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If N is a normal subgroup of G, then the quotient group G/N is a cyclic group."
    
    The witness should be a tuple (G, N) where G and N are PermutationGroups.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = False
        if hasattr(G, 'is_subgroup') and hasattr(N, 'is_subgroup'):
            if N.is_subgroup(G):
                h1 = True
                # Check normality: g * n * g^-1 in N for all generators
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if not N.contains(g * n * g_inv):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # ¬Q: The quotient group G/N is NOT a cyclic group
    try:
        neg_q = False
        if h1:
            q_order = G.order() // N.order()
            if q_order == 1:
                is_cyclic = True
            else:
                factors = factorint(q_order)
                proper_divisors = [q_order // p for p in factors]
                
                is_cyclic = False
                # G/N is cyclic iff there is an element g in G such that gN has order |G/N|
                for g in G.generate():
                    is_gen = True
                    for d in proper_divisors:
                        if N.contains(g**d):
                            is_gen = False
                            break
                    if is_gen:
                        is_cyclic = True
                        break
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The quotient group G/N is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1