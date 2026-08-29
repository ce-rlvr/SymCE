import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: K is an ideal of R",
    "¬Q: I(J + K) != IJ + IK or (I + J)K != IK + JK"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', [])
            I = witness.get('I', [])
            J = witness.get('J', [])
            K = witness.get('K', [])
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            eq = witness.get('eq', lambda a, b: a == b)
        else:
            R, I, J, K = witness
            add = lambda a, b: a + b
            mul = lambda a, b: a * b
            eq = lambda a, b: a == b
            
        def find_zero(R, add, eq):
            for z in R:
                if all(eq(add(z, a), a) and eq(add(a, z), a) for a in R):
                    return z
            return None

        def is_ring(R, add, mul, eq):
            if not R: return False
            zero = find_zero(R, add, eq)
            if zero is None: return False
            for a in R:
                for b in R:
                    if not any(eq(add(a, b), c) for c in R): return False
                    if not any(eq(mul(a, b), c) for c in R): return False
            for a in R:
                has_inv = False
                for b in R:
                    if eq(add(a, b), zero) and eq(add(b, a), zero):
                        has_inv = True
                        break
                if not has_inv: return False
            for a in R:
                for b in R:
                    for c in R:
                        if not eq(add(add(a, b), c), add(a, add(b, c))): return False
                        if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
                        if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                        if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
            for a in R:
                for b in R:
                    if not eq(add(a, b), add(b, a)): return False
            return True

        def is_ideal(I, R, add, mul, eq, zero):
            if not I: return False
            for i in I:
                if not any(eq(i, r) for r in R): return False
            if not any(eq(i, zero) for i in I): return False
            for a in I:
                for b in I:
                    if not any(eq(add(a, b), c) for c in I): return False
            for a in I:
                has_inv = False
                for b in I:
                    if eq(add(a, b), zero):
                        has_inv = True
                        break
                if not has_inv: return False
            for i in I:
                for r in R:
                    if not any(eq(mul(i, r), c) for c in I): return False
                    if not any(eq(mul(r, i), c) for c in I): return False
            return True

        def unique_elements(S, eq):
            res = []
            for x in S:
                if not any(eq(x, y) for y in res):
                    res.append(x)
            return res

        def set_add(A, B, add, eq):
            return unique_elements([add(a, b) for a in A for b in B], eq)

        def additive_closure(S, add, eq):
            closure = unique_elements(S, eq)
            added = True
            while added:
                added = False
                new_elements = []
                for a in closure:
                    for b in closure:
                        s = add(a, b)
                        if not any(eq(s, x) for x in closure) and not any(eq(s, x) for x in new_elements):
                            new_elements.append(s)
                if new_elements:
                    closure.extend(new_elements)
                    added = True
            return closure

        def ideal_mul(A, B, add, mul, eq):
            prods = unique_elements([mul(a, b) for a in A for b in B], eq)
            return additive_closure(prods, add, eq)

        def set_eq(A, B, eq):
            for a in A:
                if not any(eq(a, b) for b in B): return False
            for b in B:
                if not any(eq(a, b) for a in A): return False
            return True

        zero = find_zero(R, add, eq)
        
        try:
            h1 = is_ring(R, add, mul, eq)
        except Exception:
            h1 = False
            
        try:
            h2 = is_ideal(I, R, add, mul, eq, zero) if zero is not None else False
        except Exception:
            h2 = False
            
        try:
            h3 = is_ideal(K, R, add, mul, eq, zero) if zero is not None else False
        except Exception:
            h3 = False
            
        try:
            J_plus_K = set_add(J, K, add, eq)
            I_JplusK = ideal_mul(I, J_plus_K, add, mul, eq)
            
            IJ = ideal_mul(I, J, add, mul, eq)
            IK = ideal_mul(I, K, add, mul, eq)
            IJ_plus_IK = set_add(IJ, IK, add, eq)
            
            I_plus_J = set_add(I, J, add, eq)
            IplusJ_K = ideal_mul(I_plus_J, K, add, mul, eq)
            
            JK = ideal_mul(J, K, add, mul, eq)
            IK_plus_JK = set_add(IK, JK, add, eq)
            
            q1 = set_eq(I_JplusK, IJ_plus_IK, eq)
            q2 = set_eq(IplusJ_K, IK_plus_JK, eq)
            
            neg_q = not (q1 and q2)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]