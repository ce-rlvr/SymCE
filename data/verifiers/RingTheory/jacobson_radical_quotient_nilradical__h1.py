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

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            N = witness.get('N')
            J = witness.get('J')
        elif hasattr(witness, 'R') and hasattr(witness, 'N') and hasattr(witness, 'J'):
            R = witness.R
            N = witness.N
            J = witness.J
        else:
            R, N, J = witness
    except Exception:
        return [False, False, False]

    try:
        n_val = R.nilradical() if callable(R.nilradical) else R.nilradical
        h1 = bool(n_val == N)
    except Exception:
        h1 = False

    try:
        j_val = R.jacobson_radical() if callable(R.jacobson_radical) else R.jacobson_radical
        h2 = bool(j_val == J)
    except Exception:
        h2 = False

    try:
        try:
            if hasattr(R, 'quotient'):
                quotient_ring = R.quotient(N)
                J_mod_N = J.quotient(N)
            else:
                quotient_ring = R / N
                J_mod_N = J / N
                
            q_j_val = quotient_ring.jacobson_radical() if callable(quotient_ring.jacobson_radical) else quotient_ring.jacobson_radical
            q_holds = bool(q_j_val == J_mod_N)
        except Exception:
            # If the quotient fails (e.g., N is not an ideal in a non-commutative ring),
            # the conclusion is undefined and therefore fails.
            q_holds = False
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is the nilradical of R",
    "H_2: J is the Jacobson radical of R",
    "¬Q: The Jacobson radical of the quotient ring R/N is not equal to J/N"
]

N_HYP = 2
NEG_Q_INDEX = 2