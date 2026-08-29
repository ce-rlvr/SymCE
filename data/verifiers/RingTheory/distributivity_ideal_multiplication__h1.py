import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    if isinstance(witness, dict):
        R = witness.get('R', [])
        I = witness.get('I', [])
        J = witness.get('J', [])
        K = witness.get('K', [])
        add = witness.get('add', lambda x, y: x + y)
        mul = witness.get('mul', lambda x, y: x * y)
        eq = witness.get('eq', lambda x, y: x == y)
    elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J') and hasattr(witness, 'K'):
        R = witness.R
        I = witness.I
        J = witness.J
        K = witness.K
        add = getattr(witness, 'add', lambda x, y: x + y)
        mul = getattr(witness, 'mul', lambda x, y: x * y)
        eq = getattr(witness, 'eq', lambda x, y: x == y)
    else:
        try:
            R, I, J, K = witness
        except Exception:
            return [False, False, False, False]
        add = lambda x, y: x + y
        mul = lambda x, y: x * y
        eq = lambda x, y: x == y

    def contains(lst, item):
        for x in lst:
            try:
                if eq(x, item): return True
            except Exception:
                pass
        return False

    def is_ideal(S):
        if not S: return False
        for x in S:
            if not contains(R, x): return False
        
        zeros_list = []
        for x in R:
            try:
                is_zero = True
                for y in R:
                    if not eq(add(x, y), y) or not eq(add(y, x), y):
                        is_zero = False
                        break
                if is_zero:
                    zeros_list.append(x)
            except Exception:
                pass
        if not zeros_list: return False
        zero = zeros_list[0]
        
        if not contains(S, zero): return False
        
        for x in S:
            for y in S:
                try:
                    if not contains(S, add(x, y)): return False
                except Exception:
                    return False
                
        for x in S:
            has_inv = False
            for y in S:
                try:
                    if eq(add(x, y), zero) and eq(add(y, x), zero):
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv: return False
            
        for i in S:
            for r in R:
                try:
                    if not contains(S, mul(i, r)): return False
                    if not contains(S, mul(r, i)): return False
                except Exception:
                    return False
        return True

    try:
        h1 = is_ideal(I)
    except Exception:
        h1 = False

    try:
        h2 = is_ideal(J)
    except Exception:
        h2 = False

    try:
        h3 = is_ideal(K)
    except Exception:
        h3 = False

    try:
        def addition_closure(S):
            res = list(S)
            changed = True
            try:
                max_len = len(R)
            except Exception:
                max_len = 1000
            while changed and len(res) < max_len:
                changed = False
                new_els = []
                for x in res:
                    for y in res:
                        try:
                            s = add(x, y)
                            if not contains(res, s) and not contains(new_els, s):
                                new_els.append(s)
                                changed = True
                        except Exception:
                            pass
                res.extend(new_els)
            return res

        def ideal_add(A, B):
            res = []
            for a in A:
                for b in B:
                    try:
                        s = add(a, b)
                        if not contains(res, s):
                            res.append(s)
                    except Exception:
                        pass
            return addition_closure(res)

        def ideal_mul(A, B):
            res = []
            for a in A:
                for b in B:
                    try:
                        p = mul(a, b)
                        if not contains(res, p):
                            res.append(p)
                    except Exception:
                        pass
            return addition_closure(res)

        def set_eq(A, B):
            for a in A:
                if not contains(B, a): return False
            for b in B:
                if not contains(A, b): return False
            return True

        J_plus_K = ideal_add(J, K)
        I_plus_J = ideal_add(I, J)
        
        I_J_plus_K = ideal_mul(I, J_plus_K)
        IJ = ideal_mul(I, J)
        IK = ideal_mul(I, K)
        IJ_plus_IK = ideal_add(IJ, IK)
        
        I_plus_J_K = ideal_mul(I_plus_J, K)
        JK = ideal_mul(J, K)
        IK_plus_JK = ideal_add(IK, JK)
        
        q = set_eq(I_J_plus_K, IJ_plus_IK) and set_eq(I_plus_J_K, IK_plus_JK)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "¬Q: I(J + K) != IJ + IK or (I + J)K != IK + JK"
]

N_HYP = 3
NEG_Q_INDEX = 3