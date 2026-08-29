import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

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

def check_finite_ring(R_list, add, mul, zero, N_list, n):
    h1 = True
    if not R_list:
        return [False, False, False]
        
    # Remove duplicates while preserving order
    R_unique = []
    for x in R_list:
        if x not in R_unique:
            R_unique.append(x)
            
    subset = R_unique
    if len(R_unique) > 50:
        subset = R_unique[:50]
        
    for a in subset:
        if add(a, zero) != a or add(zero, a) != a:
            h1 = False
        has_inv = False
        for b in R_unique:
            if add(a, b) == zero:
                has_inv = True
        if not has_inv:
            h1 = False
            
        for b in subset:
            if add(a, b) != add(b, a):
                h1 = False
            if mul(a, b) != mul(b, a):
                h1 = False
            for c in subset:
                if add(add(a, b), c) != add(a, add(b, c)):
                    h1 = False
                if mul(mul(a, b), c) != mul(a, mul(b, c)):
                    h1 = False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                    h1 = False
                    
    h2 = True
    actual_N = []
    for a in R_unique:
        curr = a
        is_nil = False
        for _ in range(len(R_unique)):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, a)
        if is_nil:
            actual_N.append(a)
            
    # Check if N_list and actual_N have the same elements
    if len(N_list) != len(actual_N):
        h2 = False
    else:
        for x in N_list:
            if x not in actual_N:
                h2 = False
        for x in actual_N:
            if x not in N_list:
                h2 = False
                
    neg_q = False
    if n >= 2:
        r_not_in_N = None
        for r in R_unique:
            if r not in N_list:
                r_not_in_N = r
                break
        if r_not_in_N is not None:
            neg_q = True
            
    return [h1, h2, neg_q]

def conditions(witness):
    # 1. Try SymPy ring tuple: (R, N, n)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, N, n = witness
            if R in (sympy.ZZ, sympy.QQ) or (hasattr(R, 'is_commutative') and hasattr(R, 'is_domain') and R.is_commutative and R.is_domain):
                h1 = True
                h2 = False
                if isinstance(N, (set, list, tuple)) and len(N) == 1:
                    elem = list(N)[0]
                    if elem == 0 or (hasattr(R, 'zero') and elem == R.zero):
                        h2 = True
                neg_q = False
                if n >= 2:
                    neg_q = True
                return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try finite ring tuple: (R_list, add, mul, zero, N_list, n)
    try:
        if isinstance(witness, tuple) and len(witness) == 6:
            return check_finite_ring(*witness)
    except Exception:
        pass

    # 3. Try dictionary
    try:
        if isinstance(witness, dict):
            return check_finite_ring(
                witness['R'], witness['add'], witness['mul'],
                witness['zero'], witness['N'], witness['n']
            )
    except Exception:
        pass

    # 4. Try object with attributes
    try:
        return check_finite_ring(
            witness.R, witness.add, witness.mul,
            witness.zero, witness.N, witness.n
        )
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: N is the nilradical of R",
    "¬Q: The lower nilradical of the matrix ring M_n(R) is not equal to the matrix ring M_n(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2