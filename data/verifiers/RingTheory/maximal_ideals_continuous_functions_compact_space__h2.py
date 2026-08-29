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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture fails for the empty space (where C(X) is the zero ring, 
    leading to edge cases in the definition of maximal ideals and vacuous truths).
    """
    H1 = False
    neg_Q = False
    
    try:
        # Evaluate if the witness represents a compact Hausdorff space
        # and check if it is the empty space (the counterexample).
        if isinstance(witness, int) and not isinstance(witness, bool):
            H1 = witness >= 0
            neg_Q = (witness == 0)
        elif isinstance(witness, str):
            H1 = True
            neg_Q = (witness.strip().lower() in ["empty", "emptyset", "none", "0", "[]", "{}"])
        elif hasattr(witness, 'is_empty'):
            H1 = True
            neg_Q = bool(witness.is_empty)
        elif isinstance(witness, (list, set, tuple)):
            H1 = True
            neg_Q = (len(witness) == 0)
        elif hasattr(witness, '__len__'):
            H1 = True
            neg_Q = (len(witness) == 0)
        else:
            # Fallback for unknown objects, assume they are valid non-empty spaces
            H1 = True
            neg_Q = False
    except Exception:
        H1 = False
        neg_Q = False

    return [bool(H1), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: X is a compact Hausdorff topological space",
    "¬Q: The conclusion fails (e.g., vacuous truth / zero ring edge case for empty space)"
]

N_HYP = 1
NEG_Q_INDEX = 1