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
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the hypotheses and FAILS the conclusion.
    The witness is expected to be a tuple (I, J) or (R, I, J), or a dict with 'I' and 'J'.
    The objects should implement ideal operations (quotient, multiplication, subset).
    """
    I = None
    J = None
    
    try:
        if isinstance(witness, dict):
            I = witness.get('I')
            J = witness.get('J')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                I, J = witness
            elif len(witness) >= 3:
                I, J = witness[1], witness[2]
    except Exception:
        pass

    if I is None or J is None:
        return [False, False, False]

    # H_1: I is an ideal of R
    try:
        if hasattr(I, 'is_ideal'):
            h1 = bool(I.is_ideal() if callable(I.is_ideal) else I.is_ideal)
        else:
            # If no explicit is_ideal attribute, assume True if it supports ideal operations
            h1 = True
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        if hasattr(J, 'is_ideal'):
            h2 = bool(J.is_ideal() if callable(J.is_ideal) else J.is_ideal)
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: (I:J)J \subseteq I is FALSE
    try:
        # Compute the ideal quotient (I:J)
        if hasattr(I, 'quotient'):
            quot = I.quotient(J)
        elif hasattr(I, 'ideal_quotient'):
            quot = I.ideal_quotient(J)
        else:
            try:
                quot = I / J
            except Exception:
                quot = I // J
                
        # Compute the product (I:J)J
        prod = quot * J
        
        # Check containment prod \subseteq I
        if hasattr(prod, 'issubset'):
            subset = prod.issubset(I)
        elif hasattr(I, 'issuperset'):
            subset = I.issuperset(prod)
        else:
            subset = (prod <= I)
            
        neg_q = not bool(subset)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: (I:J)J is not contained in I"
]

N_HYP = 2
NEG_Q_INDEX = 2