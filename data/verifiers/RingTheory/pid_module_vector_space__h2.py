import sympy
from sympy import ZZ, eye, zeros, Rational, Integer
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

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
    "H_1: R is a principal ideal domain",
    "H_2: p is a prime element in R",
    "H_3: pM = {0}",
    "¬Q: M is not a vector space over R/(p)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            if 'R_is_PID' in witness:
                h1 = bool(witness.get('R_is_PID', False))
                h2 = bool(witness.get('p_is_prime', False))
                h3 = bool(witness.get('pM_is_zero', False))
                neg_q = not bool(witness.get('M_is_vector_space', True))
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'R_is_PID'):
            h1 = bool(getattr(witness, 'R_is_PID'))
            h2 = bool(getattr(witness, 'p_is_prime'))
            h3 = bool(getattr(witness, 'pM_is_zero'))
            neg_q = not bool(getattr(witness, 'M_is_vector_space'))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, p, M = witness
            
            # H1: R is a principal ideal domain
            if R == sympy.ZZ or R == 'ZZ':
                h1 = True
            elif hasattr(R, 'is_PID'):
                h1 = bool(R.is_PID)
            elif hasattr(R, 'is_principal_ideal_domain'):
                h1 = bool(R.is_principal_ideal_domain)
                
            # H2: p is a prime element in R
            if R == sympy.ZZ or R == 'ZZ':
                h2 = sympy.isprime(int(p))
            elif hasattr(R, 'is_prime'):
                h2 = bool(R.is_prime(p))
                
            # H3: pM = {0}
            if isinstance(M, PermutationGroup):
                h3 = all(getattr(g**p, 'is_Identity', False) for g in M.elements)
            elif hasattr(M, 'is_zero'):
                h3 = bool((p * M).is_zero)
            elif isinstance(M, list):
                h3 = all((p * m) == 0 or getattr(p * m, 'is_zero', False) for m in M)
                
            # neg_Q: M is not a vector space over R/(p)
            if hasattr(M, 'is_vector_space'):
                neg_q = not bool(M.is_vector_space)
            elif isinstance(M, PermutationGroup):
                # A vector space must be an abelian group
                neg_q = not M.is_abelian
            else:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]