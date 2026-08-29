import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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

def get_prop(witness, prop):
    if isinstance(witness, dict):
        return witness.get(prop)
    else:
        return getattr(witness, prop, None)

def is_ring(R, add, mul, zero):
    if zero not in R: return False
    for a in R:
        if add(a, zero) != a or add(zero, a) != a: return False
        has_inv = False
        for b in R:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in R:
        for b in R:
            if add(a, b) not in R: return False
            if mul(a, b) not in R: return False
            if add(a, b) != add(b, a): return False
            for c in R:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def conditions(witness):
    # H1: I is a two-sided ideal of R
    try:
        R = get_prop(witness, 'R')
        R_add = get_prop(witness, 'R_add')
        R_mul = get_prop(witness, 'R_mul')
        R_zero = get_prop(witness, 'R_zero')
        I = get_prop(witness, 'I')
        
        H1 = True
        if R is None or I is None or R_add is None or R_mul is None or R_zero is None:
            H1 = False
        elif not is_ring(R, R_add, R_mul, R_zero):
            H1 = False
        else:
            for i in I:
                if i not in R: H1 = False
            if R_zero not in I: H1 = False
            for i in I:
                for j in I:
                    if R_add(i, j) not in I: H1 = False
            for i in I:
                has_inv = False
                for j in I:
                    if R_add(i, j) == R_zero:
                        has_inv = True
                        break
                if not has_inv: H1 = False
            for i in I:
                for r in R:
                    if R_mul(i, r) not in I: H1 = False
                    if R_mul(r, i) not in I: H1 = False
    except Exception:
        H1 = False

    # H2: M is a left R-module
    try:
        R = get_prop(witness, 'R')
        R_add = get_prop(witness, 'R_add')
        R_mul = get_prop(witness, 'R_mul')
        M = get_prop(witness, 'M')
        M_add = get_prop(witness, 'M_add')
        M_zero = get_prop(witness, 'M_zero')
        RM_mul = get_prop(witness, 'RM_mul')
        
        H2 = True
        if M is None or M_add is None or M_zero is None or RM_mul is None:
            H2 = False
        elif M_zero not in M:
            H2 = False
        else:
            for m in M:
                if M_add(m, M_zero) != m or M_add(M_zero, m) != m: H2 = False
                has_inv = False
                for n in M:
                    if M_add(m, n) == M_zero and M_add(n, m) == M_zero:
                        has_inv = True
                        break
                if not has_inv: H2 = False
            for m1 in M:
                for m2 in M:
                    if M_add(m1, m2) not in M: H2 = False
                    if M_add(m1, m2) != M_add(m2, m1): H2 = False
                    for m3 in M:
                        if M_add(M_add(m1, m2), m3) != M_add(m1, M_add(m2, m3)): H2 = False
            for r in R:
                for m in M:
                    if RM_mul(r, m) not in M: H2 = False
            for r in R:
                for m1 in M:
                    for m2 in M:
                        if RM_mul(r, M_add(m1, m2)) != M_add(RM_mul(r, m1), RM_mul(r, m2)): H2 = False
            for r1 in R:
                for r2 in R:
                    for m in M:
                        if RM_mul(R_add(r1, r2), m) != M_add(RM_mul(r1, m), RM_mul(r2, m)): H2 = False
                        if RM_mul(R_mul(r1, r2), m) != RM_mul(r1, RM_mul(r2, m)): H2 = False
    except Exception:
        H2 = False

    # neg_Q: Hom_R(R/I, M) is not isomorphic to the submodule {m \in M | im = 0 for all i \in I}
    try:
        R = get_prop(witness, 'R')
        R_add = get_prop(witness, 'R_add')
        R_mul = get_prop(witness, 'R_mul')
        I = get_prop(witness, 'I')
        M = get_prop(witness, 'M')
        M_add = get_prop(witness, 'M_add')
        M_zero = get_prop(witness, 'M_zero')
        RM_mul = get_prop(witness, 'RM_mul')

        homs = []
        for mapping in itertools.product(M, repeat=len(R)):
            g = dict(zip(R, mapping))
            if any(g[i] != M_zero for i in I):
                continue
            is_hom = True
            for x in R:
                for y in R:
                    if g[R_add(x, y)] != M_add(g[x], g[y]):
                        is_hom = False
                        break
                if not is_hom: break
            if not is_hom: continue
            for r in R:
                for x in R:
                    if g[R_mul(r, x)] != RM_mul(r, g[x]):
                        is_hom = False
                        break
                if not is_hom: break
            if is_hom:
                homs.append(g)
                
        submod = []
        for m in M:
            if all(RM_mul(i, m) == M_zero for i in I):
                submod.append(m)
                
        if len(homs) != len(submod):
            neg_Q = True
        else:
            def hom_add(h1, h2):
                return {x: M_add(h1[x], h2[x]) for x in R}
            
            is_any_iso = False
            if len(homs) <= 6:
                for perm in itertools.permutations(submod):
                    is_iso = True
                    for i in range(len(homs)):
                        for j in range(len(homs)):
                            h_sum = hom_add(homs[i], homs[j])
                            h_sum_idx = -1
                            for k, h in enumerate(homs):
                                if h == h_sum:
                                    h_sum_idx = k
                                    break
                            if h_sum_idx == -1:
                                is_iso = False
                                break
                            m_sum = M_add(perm[i], perm[j])
                            if perm[h_sum_idx] != m_sum:
                                is_iso = False
                                break
                        if not is_iso: break
                    if is_iso:
                        is_any_iso = True
                        break
                if not is_any_iso:
                    neg_Q = True
                else:
                    neg_Q = False
            else:
                neg_Q = False
    except Exception:
        neg_Q = False

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "H_2: M is a left R-module",
    "¬Q: Hom_R(R/I, M) is not isomorphic to the submodule {m in M | im = 0 for all i in I}"
]

N_HYP = 2
NEG_Q_INDEX = 2