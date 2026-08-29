import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
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
O2 = sympy.matrices.zeros(2,2)
O3 = sympy.matrices.zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that n must be a non-negative integer.
    """
    # The witness is expected to be the dimension parameter `n` (or a tuple starting with `n`)
    if isinstance(witness, tuple):
        n = witness[0]
    else:
        n = witness
        
    try:
        # H1: Let S be the subset of M_n(F) consisting of all strictly upper triangular matrices
        # This is a definitional hypothesis. We just verify that n is a valid numeric value.
        if isinstance(n, str):
            h1_ok = False
        else:
            float(n)
            h1_ok = True
    except Exception:
        h1_ok = False
        
    try:
        # Conclusion: S is a subspace of M_n(F) with dimension n(n-1)/2
        # This conclusion is true if and only if n is a non-negative integer.
        # If n is negative or not an integer, the dimension formula n(n-1)/2 
        # does not correctly describe the dimension of a valid matrix space M_n(F).
        if n == int(n) and n >= 0:
            q_ok = True
        else:
            q_ok = False
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = True
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let S be the subset of M_n(F) consisting of all strictly upper triangular matrices",
    "¬Q: S is not a subspace of M_n(F) with dimension n(n-1)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1