import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# (No specific named objects required for this ring theory conjecture, 
# as witnesses are typically lists of integers representing subsets of ZZ)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "The localization of a Dedekind domain at a multiplicatively closed subset is a Dedekind domain."
    
    The dropped hypothesis is that 0 is not in S. If 0 in S, S^{-1}R is the zero ring,
    which is not an integral domain, and therefore not a Dedekind domain.
    
    Expected witness format:
      - A list of integers representing the subset S of ZZ.
      - OR a tuple (R, S) where R is a string like "ZZ" and S is a list of elements.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = "ZZ"
            S = witness
            
        S = list(S)
    except Exception:
        return [False, False, False]

    # H1: R is a Dedekind domain
    try:
        # We accept standard Dedekind domains like ZZ or QQ
        h1 = (R in ["ZZ", "QQ", sympy.S.Integers, sympy.S.Rationals])
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        if not S:
            h2 = False
        else:
            # Check if all elements belong to R (if R is ZZ)
            if R in ["ZZ", sympy.S.Integers] and not all(isinstance(x, (int, sympy.Integer)) for x in S):
                h2 = False
            else:
                # Check multiplicative closure
                h2 = all(a * b in S for a in S for b in S)
    except Exception:
        h2 = False

    # neg_Q: S^{-1}R is NOT a Dedekind domain
    try:
        # S^{-1}R is a Dedekind domain iff it is an integral domain (since R is Dedekind).
        # It is an integral domain iff 0 is not in S.
        # Thus, it is NOT a Dedekind domain iff 0 is in S.
        neg_q = (0 in S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}R is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2