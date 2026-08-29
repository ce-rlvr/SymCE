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

def conditions(witness) -> list[bool]:
    try:
        # The hypothesis defines d(n) for an integer n.
        # We verify that the witness is an integer.
        if isinstance(witness, bool):
            h1_ok = False
        else:
            n = int(witness)
            h1_ok = (n == witness)
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n = int(witness)
            
            # Evaluate LHS: d(n) is an odd integer
            if n == 0:
                # Every positive integer divides 0, so d(0) is infinite (not an odd integer)
                lhs = False
            else:
                d_n = len(sympy.divisors(n))
                lhs = (d_n % 2 == 1)
            
            # Evaluate RHS: there exists an integer k such that n = k^2
            if n < 0:
                rhs = False
            else:
                root = math.isqrt(n)
                rhs = (root * root == n)
                
            # The conclusion is LHS <-> RHS.
            # The negated conclusion is that the biconditional fails (LHS XOR RHS).
            neg_q_ok = (lhs != rhs)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: d(n) is the number of positive divisors of n",
    "¬Q: d(n) is an odd integer iff n is a perfect square FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1