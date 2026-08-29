import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, S, f, e = witness
        else:
            R = witness.R
            S = witness.S
            f = witness.f
            e = witness.e
        
        R = list(R)
        S = list(S)
    except Exception:
        return [False, False, False, False]

    def apply_f(val):
        return f(val) if callable(f) else f[val]

    def add(ring, a, b):
        if hasattr(ring, 'add'): return ring.add(a, b)
        return a + b

    def mul(ring, a, b):
        if hasattr(ring, 'mul'): return ring.mul(a, b)
        return a * b

    def eq(a, b):
        return bool(a == b)

    # H1: f is a surjective ring homomorphism
    try:
        image = [apply_f(val) for val in R]
        H1_surj = all(any(eq(val, img) for img in image) for val in S)
        H1_hom = True
        for a in R:
            for b in R:
                if not eq(apply_f(add(R, a, b)), add(S, apply_f(a), apply_f(b))):
                    H1_hom = False
                if not eq(apply_f(mul(R, a, b)), mul(S, apply_f(a), apply_f(b))):
                    H1_hom = False
        H1 = H1_surj and H1_hom
    except Exception:
        H1 = False

    # H2: ker(f) is a nil ideal
    try:
        zero_S = None
        for val in S:
            if eq(add(S, val, val), val):
                zero_S = val
                break
        
        zero_R = None
        for val in R:
            if eq(add(R, val, val), val):
                zero_R = val
                break

        if zero_S is None or zero_R is None:
            H2 = False
        else:
            ker = [val for val in R if eq(apply_f(val), zero_S)]
            H2 = True
            for val in ker:
                is_nil = False
                curr = val
                for _ in range(len(R)):
                    if eq(curr, zero_R):
                        is_nil = True
                        break
                    curr = mul(R, curr, val)
                if not is_nil:
                    H2 = False
                    break
    except Exception:
        H2 = False

    # H3: e is an idempotent element in S
    try:
        H3 = eq(mul(S, e, e), e) and any(eq(val, e) for val in S)
    except Exception:
        H3 = False

    # neg_Q: no idempotent E in R such that f(E) = e
    try:
        exists = False
        for E in R:
            if eq(mul(R, E, E), E) and eq(apply_f(E), e):
                exists = True
                break
        neg_Q = not exists
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism",
    "H_2: the kernel of f is a nil ideal",
    "H_3: e is an idempotent element in S",
    "¬Q: There does not exist an idempotent element E in R such that f(E) = e"
]

N_HYP = 3
NEG_Q_INDEX = 3