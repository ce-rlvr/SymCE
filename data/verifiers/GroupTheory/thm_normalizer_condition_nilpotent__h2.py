import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
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
V4 = PermutationGroup(
    Permutation([[0, 1], [2, 3]]),
    Permutation([[0, 2], [1, 3]])
)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H) or a dict {'G': G, 'H': H}.
    If a single group is provided, it is assumed that H = G.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = witness
            
        if G is None or H is None:
            return [False, False]
    except Exception:
        return [False, False]
        
    # Hypothesis 1: G is a nilpotent group
    try:
        nilpotent = G.is_nilpotent
        if callable(nilpotent):
            nilpotent = nilpotent()
        h1 = bool(nilpotent)
    except Exception:
        h1 = False
        
    # Negated Conclusion: H is NOT strictly contained in the normalizer N_G(H)
    try:
        # First, ensure H is actually a subgroup of G
        is_subgroup = all(h in G for h in H.generators)
        if not is_subgroup:
            neg_q = False
        else:
            strict_containment = False
            # Check if there exists any element g in G \ H that normalizes H
            for g in G.elements:
                if g not in H:
                    normalizes = True
                    for h in H.generators:
                        if (g * h * ~g) not in H:
                            normalizes = False
                            break
                    if normalizes:
                        strict_containment = True
                        break
            # The conclusion fails (neg_q is True) if there is NO strict containment
            neg_q = not strict_containment
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: H is NOT strictly contained in the normalizer N_G(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1