import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness):
    try:
        R = list(witness.R)
        S = list(witness.S)
        n = int(witness.n)
        f = witness.f
        
        if hasattr(witness, 'add_R'):
            add_R = witness.add_R
            mul_R = witness.mul_R
        else:
            add_R = lambda a, b: a + b
            mul_R = lambda a, b: a * b
            
        if hasattr(witness, 'add_S'):
            add_S = witness.add_S
            mul_S = witness.mul_S
        else:
            add_S = lambda a, b: a + b
            mul_S = lambda a, b: a * b
            
        zero_R = witness.zero_R
        one_R = witness.one_R
        zero_S = witness.zero_S
        one_S = witness.one_S
    except Exception:
        return [False, False, False, False]

    def eq(a, b):
        try:
            return bool(a == b)
        except Exception:
            return False

    def is_ring(elements, add, mul, zero, one):
        try:
            if not any(eq(zero, x) for x in elements): return False
            if not any(eq(one, x) for x in elements): return False
            
            for a in elements:
                for b in elements:
                    if not any(eq(add(a, b), x) for x in elements): return False
                    if not any(eq(mul(a, b), x) for x in elements): return False
            
            for a in elements:
                if not eq(add(a, zero), a) or not eq(add(zero, a), a): return False
            
            for a in elements:
                has_inv = False
                for b in elements:
                    if eq(add(a, b), zero) and eq(add(b, a), zero):
                        has_inv = True
                        break
                if not has_inv: return False
            
            for a in elements:
                for b in elements:
                    if not eq(add(a, b), add(b, a)): return False
                    for c in elements:
                        if not eq(add(add(a, b), c), add(a, add(b, c))): return False
            
            for a in elements:
                if not eq(mul(a, one), a) or not eq(mul(one, a), a): return False
            
            for a in elements:
                for b in elements:
                    for c in elements:
                        if not eq(mul(mul(a, b), c), mul(a, mul(b, c))): return False
            
            for a in elements:
                for b in elements:
                    for c in elements:
                        if not eq(mul(a, add(b, c)), add(mul(a, b), mul(a, c))): return False
                        if not eq(mul(add(a, b), c), add(mul(a, c), mul(b, c))): return False
            return True
        except Exception:
            return False

    try:
        h1 = is_ring(R, add_R, mul_R, zero_R, one_R) and is_ring(S, add_S, mul_S, zero_S, one_S)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    try:
        h3 = True
        if not eq(f(one_R), one_S):
            h3 = False
        if not eq(f(zero_R), zero_S):
            h3 = False
        for a in R:
            for b in R:
                if not eq(f(add_R(a, b)), add_S(f(a), f(b))):
                    h3 = False
                if not eq(f(mul_R(a, b)), mul_S(f(a), f(b))):
                    h3 = False
    except Exception:
        h3 = False

    try:
        K = [x for x in R if eq(f(x), zero_S)]
        has_id = False
        for e in K:
            is_id = True
            for x in K:
                if not eq(mul_R(e, x), x) or not eq(mul_R(x, e), x):
                    is_id = False
                    break
            if is_id:
                has_id = True
                break
        neg_q = not has_id
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: n is a positive integer",
    "H_3: F is the induced ring homomorphism from M_n(R) to M_n(S) that applies f to each entry",
    "¬Q: The kernel of F is not the matrix ring M_n(K) consisting of all n by n matrices with entries in the kernel of f"
]

N_HYP = 3
NEG_Q_INDEX = 3