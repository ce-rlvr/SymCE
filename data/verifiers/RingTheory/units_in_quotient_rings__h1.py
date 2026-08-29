import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: I is a proper two-sided ideal of R",
    "H_2: u is a unit in R",
    "¬Q: The coset u + I is not a unit in the quotient ring R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        R, I, u = witness
        if not hasattr(R, '__iter__') or not hasattr(I, '__iter__'):
            return [False, False, False]
        R = list(R)
        I = list(I)
        if len(R) > 1000:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # Find identity
    try:
        identity = None
        for e in R:
            is_id = True
            for r in R:
                try:
                    if not eq(e * r, r) or not eq(r * e, r):
                        is_id = False
                        break
                except Exception:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
    except Exception:
        identity = None

    # H1: I is a proper two-sided ideal of R
    h1 = False
    try:
        is_subset = all(any(eq(a, r) for r in R) for a in I)
        if is_subset and len(I) < len(R):
            if len(I) > 0:
                is_subgroup = True
                for a in I:
                    for b in I:
                        try:
                            diff = a - b
                            if not any(eq(diff, c) for c in I):
                                is_subgroup = False
                                break
                        except Exception:
                            if not any(eq(a, b + c) for c in I):
                                is_subgroup = False
                                break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    is_ideal = True
                    for a in I:
                        for r in R:
                            try:
                                ra = r * a
                                if not any(eq(ra, c) for c in I):
                                    is_ideal = False
                                    break
                            except Exception:
                                is_ideal = False
                                break
                            
                            try:
                                ar = a * r
                                if not any(eq(ar, c) for c in I):
                                    is_ideal = False
                                    break
                            except Exception:
                                is_ideal = False
                                break
                        if not is_ideal:
                            break
                    h1 = is_ideal
    except Exception:
        h1 = False

    # H2: u is a unit in R
    h2 = False
    try:
        if identity is not None and any(eq(u, r) for r in R):
            for v in R:
                try:
                    if eq(u * v, identity) and eq(v * u, identity):
                        h2 = True
                        break
                except Exception:
                    pass
    except Exception:
        h2 = False

    # neg_Q: u + I is NOT a unit in R/I
    neg_q = False
    try:
        if identity is not None:
            is_unit_in_quotient = False
            for v in R:
                try:
                    uv = u * v
                    vu = v * u
                    try:
                        uv_minus_1 = uv - identity
                        vu_minus_1 = vu - identity
                        uv_in_coset = any(eq(uv_minus_1, c) for c in I)
                        vu_in_coset = any(eq(vu_minus_1, c) for c in I)
                    except Exception:
                        uv_in_coset = any(eq(uv, identity + c) for c in I)
                        vu_in_coset = any(eq(vu, identity + c) for c in I)
                        
                    if uv_in_coset and vu_in_coset:
                        is_unit_in_quotient = True
                        break
                except Exception:
                    pass
            neg_q = not is_unit_in_quotient
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]