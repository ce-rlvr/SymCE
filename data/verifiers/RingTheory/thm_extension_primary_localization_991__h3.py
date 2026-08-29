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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal in R",
    "¬Q: The extended ideal Q R_P is not a P R_P-primary ideal in the localization R_P"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (R_str, p, q) representing:
      - R_str: The commutative ring R (supported: 'ZZ' or 'QQ[x]')
      - p: A generator for the prime ideal P in R
      - q: A generator for the ideal Q in R
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        
        R_str, p, q = witness
        
        h1 = False
        h2 = False
        neg_q = False
        
        if R_str == 'ZZ':
            h1 = True
            try:
                p_int = int(p)
                q_int = int(q)
            except Exception:
                return [False, False, False]
            
            if p_int == 0:
                h2 = True
                # In ZZ_{(0)} = QQ, P R_P = (0).
                # Q R_P is (0)-primary iff Q R_P = (0) iff q_int == 0.
                neg_q = (q_int != 0)
            else:
                h2 = sympy.isprime(abs(p_int))
                if h2:
                    # P R_P is p ZZ_{(p)}.
                    # Q R_P is P R_P-primary iff q_int != 0 and q_int % p_int == 0.
                    is_primary = (q_int != 0) and (q_int % p_int == 0)
                    neg_q = not is_primary
                else:
                    neg_q = False
                    
        elif R_str == 'QQ[x]':
            h1 = True
            try:
                p_poly = sympy.Poly(p, sympy.abc.x, domain='QQ')
                q_poly = sympy.Poly(q, sympy.abc.x, domain='QQ')
            except Exception:
                return [False, False, False]
            
            if p_poly.is_zero:
                h2 = True
                neg_q = not q_poly.is_zero
            else:
                h2 = p_poly.is_irreducible
                if h2:
                    is_primary = (not q_poly.is_zero) and (sympy.rem(q_poly.as_expr(), p_poly.as_expr(), sympy.abc.x) == 0)
                    neg_q = not is_primary
                else:
                    neg_q = False
                    
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]