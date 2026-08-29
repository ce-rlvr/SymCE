import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
from sympy.abc import x, y, z
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The number of isomorphism classes of abelian groups of order p^n is not equal to P(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
        else:
            p, n = witness
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # ¬Q: The number of isomorphism classes of abelian groups of order p^n is not equal to P(n)
    try:
        order = p**n
        
        # Calculate LHS: number of abelian groups of order p^n
        try:
            if isinstance(order, (int, sympy.Integer)):
                ord_val = int(order)
            elif hasattr(order, 'is_Integer') and order.is_Integer:
                ord_val = int(order)
            elif order == int(order):
                ord_val = int(order)
            else:
                ord_val = None
        except Exception:
            ord_val = None

        if ord_val is not None and ord_val >= 1:
            if ord_val == 1:
                lhs = 1
            else:
                factors = sympy.factorint(ord_val)
                lhs = 1
                for q, a in factors.items():
                    lhs *= sympy.ntheory.npartitions(a)
        else:
            lhs = 0

        # Calculate RHS: P(n)
        try:
            if isinstance(n, (int, sympy.Integer)):
                n_val = int(n)
            elif hasattr(n, 'is_Integer') and n.is_Integer:
                n_val = int(n)
            elif n == int(n):
                n_val = int(n)
            else:
                n_val = None
        except Exception:
            n_val = None

        if n_val is not None and n_val >= 0:
            rhs = sympy.ntheory.npartitions(n_val)
        else:
            rhs = None

        if rhs is None:
            neg_q = True
        else:
            neg_q = (lhs != rhs)

    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]