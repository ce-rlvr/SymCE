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

# Top-level setup: named object bindings
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A = witness
        m, n = A.shape
        
        # The conclusion states: there exists an n x n real orthogonal matrix Q
        # such that Q^T (A^T A) Q = A A^T.
        # A^T A is an n x n matrix, so Q^T (A^T A) Q is also n x n.
        # A A^T is an m x m matrix.
        # For them to be equal, we must have m = n.
        # If A is a real square matrix (m = n), A^T A and A A^T are real symmetric matrices
        # with the same eigenvalues, so they are always orthogonally similar.
        # Therefore, the conclusion fails if and only if A is not square.
        neg_Q = bool(m != n)
        
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: There does not exist an n x n real orthogonal matrix Q such that Q^T (A^T A) Q = A A^T"
]

N_HYP = 0
NEG_Q_INDEX = 0