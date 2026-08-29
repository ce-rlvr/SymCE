import sympy
from sympy import eye, zeros
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z1 = list(range(1))
Z2 = list(range(2))
Z3 = list(range(3))
Z4 = list(range(4))
Z5 = list(range(5))
Z6 = list(range(6))
Z8 = list(range(8))
Z10 = list(range(10))
Z12 = list(range(12))

CONDITION_LABELS = [
    "H_1: S is a subring of R",
    "H_2: S contains the multiplicative identity of R",
    "¬Q: S is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        S, R = witness
    except Exception:
        return [False, False, False]
        
    h1 = False
    h2 = False
    neg_q = False
    
    # Pre-process R and S
    try:
        if isinstance(R, (list, tuple, set)) and all(isinstance(x, int) for x in R):
            n = len(R)
            if set(R) == set(range(n)):
                R = n
    except Exception:
        pass

    # Integer case (representing Z_n)
    if isinstance(R, int) and R >= 1:
        n = R
        try:
            if isinstance(S, (list, tuple, set)):
                S_set = set(S)
            elif isinstance(S, int) and S == R:
                S_set = set(range(n))
            else:
                S_set = set()
        except Exception:
            S_set = set()
            
        # H1: S is a subring of R
        try:
            if S_set.issubset(set(range(n))) and len(S_set) > 0:
                closed_sub = all(((a - b) % n) in S_set for a in S_set for b in S_set)
                closed_mul = all(((a * b) % n) in S_set for a in S_set for b in S_set)
                if closed_sub and closed_mul:
                    h1 = True
        except Exception:
            h1 = False
            
        # H2: S contains the multiplicative identity of R
        try:
            if (1 % n) in S_set:
                h2 = True
        except Exception:
            h2 = False
            
        # ¬Q: S is not an integral domain
        try:
            if n == 1:
                neg_q = True
            else:
                closed_sub = all(((a - b) % n) in S_set for a in S_set for b in S_set)
                closed_mul = all(((a * b) % n) in S_set for a in S_set for b in S_set)
                if not (closed_sub and closed_mul and len(S_set) > 0):
                    neg_q = True
                else:
                    id_S = None
                    for e in S_set:
                        if all((e * a) % n == a for a in S_set):
                            id_S = e
                            break
                    
                    if id_S is None or id_S == 0:
                        neg_q = True
                    else:
                        has_zero_divisors = False
                        for a in S_set:
                            for b in S_set:
                                if a != 0 and b != 0 and (a * b) % n == 0:
                                    has_zero_divisors = True
                                    break
                            if has_zero_divisors:
                                break
                        
                        if has_zero_divisors:
                            neg_q = True
                        else:
                            neg_q = False
        except Exception:
            neg_q = False

    # Matrix case
    elif isinstance(R, (list, tuple, set)) and all(hasattr(m, 'is_Matrix') and m.is_Matrix for m in R):
        try:
            R_set = list(R)
            S_set = list(S) if isinstance(S, (list, tuple, set)) else []
        except Exception:
            R_set = []
            S_set = []
            
        def in_list(mat, lst):
            return any(mat == x for x in lst)
            
        # H1: S is a subring of R
        try:
            is_subset = all(in_list(s, R_set) for s in S_set)
            if is_subset and len(S_set) > 0:
                closed_sub = all(in_list(a - b, S_set) for a in S_set for b in S_set)
                closed_mul = all(in_list(a * b, S_set) for a in S_set for b in S_set)
                if closed_sub and closed_mul:
                    h1 = True
        except Exception:
            h1 = False
            
        # H2: S contains the multiplicative identity of R
        try:
            id_R = None
            for e in R_set:
                if all(e * a == a and a * e == a for a in R_set):
                    id_R = e
                    break
            if id_R is not None and in_list(id_R, S_set):
                h2 = True
        except Exception:
            h2 = False
            
        # ¬Q: S is not an integral domain
        try:
            closed_sub = all(in_list(a - b, S_set) for a in S_set for b in S_set)
            closed_mul = all(in_list(a * b, S_set) for a in S_set for b in S_set)
            if not (closed_sub and closed_mul and len(S_set) > 0):
                neg_q = True
            else:
                is_comm = all(a * b == b * a for a in S_set for b in S_set)
                
                zero_S = None
                for z in S_set:
                    if all(z + a == a and a + z == a for a in S_set):
                        zero_S = z
                        break
                        
                id_S = None
                for e in S_set:
                    if all(e * a == a and a * e == a for a in S_set):
                        id_S = e
                        break
                        
                if not is_comm:
                    neg_q = True
                elif id_S is None:
                    neg_q = True
                elif zero_S is not None and id_S == zero_S:
                    neg_q = True
                else:
                    has_zd = False
                    for a in S_set:
                        for b in S_set:
                            if a != zero_S and b != zero_S and a * b == zero_S:
                                has_zd = True
                                break
                        if has_zd:
                            break
                    if has_zd:
                        neg_q = True
        except Exception:
            neg_q = False

    # SymPy domain case
    elif R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
        try:
            if S == R:
                h1 = True
                h2 = True
        except Exception:
            pass
        neg_q = False

    return [h1, h2, neg_q]