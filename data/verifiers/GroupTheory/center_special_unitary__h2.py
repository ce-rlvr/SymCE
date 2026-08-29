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
    Checks if the witness is a counterexample to the conjecture.
    The witness is expected to be the integer n, representing the parameter for SU(n).
    """
    try:
        # H_1: G is the special unitary group SU(n) over the complex numbers
        # This implies n must be a non-negative integer.
        h1 = isinstance(witness, (int, sympy.Integer)) and witness >= 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            # Conclusion: The center of G is isomorphic to the cyclic group Z/nZ.
            # For n >= 1, the center of SU(n) is isomorphic to Z/nZ.
            # For n = 0, SU(0) is the trivial group, so its center is trivial.
            # However, Z/0Z is isomorphic to Z, which is infinite.
            # Thus, the conclusion fails (they are not isomorphic) when n = 0.
            neg_q = (n == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the special unitary group SU(n) over the complex numbers",
    "¬Q: The center of G is not isomorphic to the cyclic group Z/nZ"
]

N_HYP = 1
NEG_Q_INDEX = 1