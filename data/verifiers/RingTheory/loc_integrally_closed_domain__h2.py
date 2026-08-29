import sympy
from sympy import ZZ, QQ, Symbol
from sympy.abc import x, y, z
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is an integrally closed domain",
    "H_2: 0 is not an element of S",
    "¬Q: The localized ring S^{-1}R is not an integrally closed domain"
]

def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False, False]

    # H1: R is an integrally closed domain
    h1_ok = False
    try:
        if R == sympy.S.Integers:
            R = ZZ
            
        def is_icd(domain):
            if domain == ZZ or domain == QQ:
                return True
            if hasattr(domain, 'domain') and hasattr(domain, 'symbols'):
                return is_icd(domain.domain)
            return False
            
        h1_ok = is_icd(R)
    except Exception:
        h1_ok = False

    # H2: 0 is not an element of S
    h2_ok = False
    try:
        zero = R.zero if hasattr(R, 'zero') else 0
        h2_ok = (zero not in S) and (0 not in S)
        
        # Verify S is a subset of R
        subset_ok = True
        for s in S:
            if hasattr(R, 'of_type'):
                if not R.of_type(s):
                    if R == ZZ and isinstance(s, int):
                        continue
                    subset_ok = False
                    break
            else:
                if s not in R:
                    subset_ok = False
                    break
        if not subset_ok:
            h2_ok = False
    except Exception:
        h2_ok = False

    # neg_Q: S^-1 R is NOT an integrally closed domain
    neg_q_ok = False
    try:
        def is_S_inv_R_icd(R, S):
            if not S:
                return False
            for s1 in S:
                for s2 in S:
                    prod = R.mul(s1, s2) if hasattr(R, 'mul') else s1 * s2
                    divides = False
                    for s3 in S:
                        if hasattr(R, 'exquo'):
                            try:
                                R.exquo(s3, prod)
                                divides = True
                                break
                            except Exception:
                                pass
                        else:
                            if prod != 0 and s3 % prod == 0:
                                divides = True
                                break
                    if not divides:
                        return False
                    
                    sum_s = R.add(s1, s2) if hasattr(R, 'add') else s1 + s2
                    divides_add = False
                    for s3 in S:
                        val = R.mul(s3, sum_s) if hasattr(R, 'mul') else s3 * sum_s
                        if hasattr(R, 'exquo'):
                            try:
                                R.exquo(val, prod)
                                divides_add = True
                                break
                            except Exception:
                                pass
                        else:
                            if prod != 0 and val % prod == 0:
                                divides_add = True
                                break
                    if not divides_add:
                        return False
            return True
            
        neg_q_ok = not is_S_inv_R_icd(R, S)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]