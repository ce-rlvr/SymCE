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
    e = witness
    # If witness is provided as a tuple (R, e), extract e
    if isinstance(witness, tuple) and len(witness) == 2:
        e = witness[1]
        
    try:
        # H_1: R is an integral domain
        # We verify that e belongs to a commutative ring without zero divisors.
        # In SymPy, standard commutative expressions (Expr) and Python numbers 
        # belong to the complex field (or subrings like ZZ), which are integral domains.
        if isinstance(e, sympy.MatrixBase):
            h1 = False
        elif isinstance(e, sympy.Expr):
            h1 = e.is_commutative is not False
        elif isinstance(e, (int, float, complex)):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: e != 0 and e != 1
        if isinstance(e, sympy.Expr):
            is_zero = sympy.simplify(e) == 0
            is_one = sympy.simplify(e - 1) == 0
            neg_q = not (is_zero or is_one)
        else:
            neg_q = (e != 0 and e != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: e is neither 0 nor 1"
]

N_HYP = 1
NEG_Q_INDEX = 1