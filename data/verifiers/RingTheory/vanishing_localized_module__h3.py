import sympy
from sympy import *
import itertools
import math

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "¬Q: S^{-1}M = 0 is not equivalent to (for all m in M, exists s in S such that sm = 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness is expected to be a tuple (n, m, S) or a dict {'n': n, 'm': m, 'S': S}
    where:
      - n is the modulus of the ring R = Z/nZ (n=0 means R = Z)
      - m is the modulus of the module M = Z/mZ (m=0 means M = Z)
      - S is a list/set/tuple of integers representing the subset S of R
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
            S = witness.get('S')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n, m, S = witness
        else:
            return [False, False, False]
            
        if not (isinstance(n, int) and isinstance(m, int) and isinstance(S, (list, set, tuple))):
            return [False, False, False]
        if not all(isinstance(s, int) for s in S):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    # Z/nZ is always a commutative ring for any integer n >= 0
    h1 = True

    # H2: M is an R-module
    # Z/mZ is a Z/nZ module iff n % m == 0 (for m > 0) or (n == 0 if m == 0)
    try:
        if m < 0 or n < 0:
            h2 = False
        elif m == 0:
            h2 = (n == 0)
        else:
            h2 = (n % m == 0)
    except Exception:
        h2 = False

    # neg_Q: LHS != RHS
    try:
        # LHS: S^{-1}M = 0
        # This means the multiplicative closure of S contains an element that annihilates M.
        if m == 0:
            # For M = Z, the only annihilator is 0.
            # Since Z has no zero divisors, 0 is in the multiplicative closure of S iff 0 is in S.
            lhs = (0 in S)
        else:
            # For M = Z/mZ, we compute the multiplicative closure of S modulo m.
            closure = set([1 % m])
            queue = [1 % m]
            lhs = False
            if 0 in closure:
                lhs = True
            while queue and not lhs:
                curr = queue.pop(0)
                for s in S:
                    nxt = (curr * s) % m
                    if nxt not in closure:
                        closure.add(nxt)
                        queue.append(nxt)
                        if nxt == 0:
                            lhs = True
                            break

        # RHS: for all x in M, exists s in S such that s*x = 0
        if m == 0:
            # For M = Z, we need s*x = 0 for all x. For x=1, s*1=0 => s=0.
            # So 0 must be in S. If 0 is in S, then 0*x = 0 for all x.
            rhs = (0 in S)
        else:
            rhs = True
            for x in range(m):
                found = False
                for s in S:
                    if (s * x) % m == 0:
                        found = True
                        break
                if not found:
                    rhs = False
                    break
                    
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]