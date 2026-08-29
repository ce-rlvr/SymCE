import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
import functools
import z3

# Top-level setup for potential witness elements
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

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: K is an ideal of R",
    "H_4: I \\subseteq J",
    "¬Q: IK \\not\\subseteq JK"
]

def is_ring(R):
    if not isinstance(R, (list, tuple, set)): return False
    R_list = list(R)
    if not R_list: return False
    if len(R_list) > 200: return False
    for a in R_list:
        for b in R_list:
            if (a + b) not in R_list: return False
            if (a * b) not in R_list: return False
            if (a - b) not in R_list: return False
    has_id = False
    for e in R_list:
        is_id = True
        for a in R_list:
            if not (a * e == a) or not (e * a == a):
                is_id = False
                break
        if is_id:
            has_id = True
            break
    if not has_id: return False
    return True

def is_ideal(I, R):
    if not isinstance(I, (list, tuple, set)): return False
    I_list = list(I)
    R_list = list(R)
    if not I_list: return False
    if len(I_list) > 200 or len(R_list) > 200: return False
    for i in I_list:
        if i not in R_list: return False
    for a in I_list:
        for b in I_list:
            if (a + b) not in I_list: return False
            if (a - b) not in I_list: return False
    for i in I_list:
        for r in R_list:
            if (i * r) not in I_list: return False
            if (r * i) not in I_list: return False
    return True

def is_subset(A, B):
    if not isinstance(A, (list, tuple, set)): return False
    if not isinstance(B, (list, tuple, set)): return False
    B_list = list(B)
    for a in A:
        if a not in B_list:
            return False
    return True

def ideal_product(I, K):
    base = []
    for i in I:
        for k in K:
            prod = i * k
            if prod not in base:
                base.append(prod)
    
    closure = list(base)
    added = True
    while added:
        added = False
        new_elements = []
        for x in closure:
            for y in base:
                s = x + y
                if s not in closure and s not in new_elements:
                    new_elements.append(s)
                d = x - y
                if d not in closure and d not in new_elements:
                    new_elements.append(d)
        if new_elements:
            closure.extend(new_elements)
            added = True
        if len(closure) > 200:
            break
    return closure

def set_product(J, K):
    res = []
    for j in J:
        for k in K:
            prod = j * k
            if prod not in res:
                res.append(prod)
    return res

def conditions(witness):
    try:
        R, I, J, K = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: R is a ring
    try:
        if hasattr(R, 'is_ring'):
            h1 = bool(R.is_ring())
        elif hasattr(R, 'is_Ring'):
            h1 = True
        else:
            h1 = is_ring(R)
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        if hasattr(I, 'is_ideal'):
            h2 = bool(I.is_ideal(R))
        elif hasattr(I, 'is_Ideal'):
            h2 = (I.ring == R)
        else:
            h2 = is_ideal(I, R)
    except Exception:
        h2 = False

    # H3: K is an ideal of R
    try:
        if hasattr(K, 'is_ideal'):
            h3 = bool(K.is_ideal(R))
        elif hasattr(K, 'is_Ideal'):
            h3 = (K.ring == R)
        else:
            h3 = is_ideal(K, R)
    except Exception:
        h3 = False

    # H4: I \subseteq J
    try:
        if hasattr(I, 'issubset'):
            h4 = bool(I.issubset(J))
        elif hasattr(I, 'subset'):
            h4 = bool(I.subset(J))
        else:
            h4 = is_subset(I, J)
    except Exception:
        h4 = False

    # neg_Q: IK \not\subseteq JK
    try:
        neg_q = False
        computed = False
        
        # Try using overloaded operators first
        try:
            IK = I * K
            JK = J * K
            if hasattr(IK, 'issubset'):
                neg_q = not bool(IK.issubset(JK))
                computed = True
            elif hasattr(IK, 'subset'):
                neg_q = not bool(IK.subset(JK))
                computed = True
            elif isinstance(IK, (list, tuple, set)) and isinstance(JK, (list, tuple, set)):
                neg_q = not is_subset(IK, JK)
                computed = True
        except Exception:
            pass
            
        if not computed:
            # Fallback to finite sets
            IK = ideal_product(I, K)
            if is_ideal(J, R):
                JK = ideal_product(J, K)
            else:
                JK = set_product(J, K)
            neg_q = not is_subset(IK, JK)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]