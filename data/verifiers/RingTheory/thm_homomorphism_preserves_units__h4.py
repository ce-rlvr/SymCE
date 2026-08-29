import sympy
from sympy import ZZ, QQ
import math

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard integer rings (Z/nZ represented by integers) and SymPy domains.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def is_ring(ring):
    if isinstance(ring, int) and ring > 1:
        return True
    if hasattr(ring, 'is_ring') and ring.is_ring:
        return True
    return False

def get_one(ring):
    if isinstance(ring, int):
        return 1
    if hasattr(ring, 'one'):
        return ring.one
    return 1

def get_zero(ring):
    if isinstance(ring, int):
        return 0
    if hasattr(ring, 'zero'):
        return ring.zero
    return 0

def get_elements(ring):
    if isinstance(ring, int):
        return list(range(ring))
    if hasattr(ring, 'from_int'):
        return [ring.from_int(x) for x in [0, 1, 2, -1, -2, 3]]
    try:
        return [ring.zero, ring.one, ring.one + ring.one, ring.zero - ring.one]
    except Exception:
        return [0, 1, 2, -1]

def add(ring, a, b):
    if isinstance(ring, int):
        return (a + b) % ring
    return a + b

def mul(ring, a, b):
    if isinstance(ring, int):
        return (a * b) % ring
    return a * b

def exquo(ring, a, b):
    if isinstance(ring, int):
        if a == 1:
            return pow(b, -1, ring)
        else:
            inv = pow(b, -1, ring)
            return (a * inv) % ring
    if hasattr(ring, 'exquo'):
        try:
            a_elem = ring(a) if hasattr(ring, '__call__') else a
            b_elem = ring(b) if hasattr(ring, '__call__') else b
            return ring.exquo(a_elem, b_elem)
        except Exception:
            return ring.exquo(a, b)
    res = a / b
    if int(res) == res:
        return int(res)
    raise ValueError("Not exact quotient")

def apply_f(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def conditions(witness) -> list[bool]:
    """
    witness: tuple (R, S, f, u) or dict with keys 'R', 'S', 'f', 'u'
    where R and S are rings, f is a homomorphism, and u is an element of R.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
            u = witness.get('u')
        else:
            R, S, f, u = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings with identity
    try:
        h1 = is_ring(R) and is_ring(S)
    except Exception:
        h1 = False

    # H_2: f is a ring homomorphism
    try:
        h2 = True
        elems_R = get_elements(R)
        for a in elems_R:
            for b in elems_R:
                # Preserves addition: f(a+b) == f(a) + f(b)
                sum_ab = add(R, a, b)
                f_sum = apply_f(f, sum_ab)
                sum_f = add(S, apply_f(f, a), apply_f(f, b))
                if f_sum != sum_f:
                    h2 = False
                    break
                
                # Preserves multiplication: f(a*b) == f(a) * f(b)
                mul_ab = mul(R, a, b)
                f_mul = apply_f(f, mul_ab)
                mul_f = mul(S, apply_f(f, a), apply_f(f, b))
                if f_mul != mul_f:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # H_3: f(1_R) = 1_S
    try:
        h3 = apply_f(f, get_one(R)) == get_one(S)
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails.
    # Conclusion: f(u) is a unit in S and f(u^{-1}) = f(u)^{-1}
    try:
        fu = apply_f(f, u)
        
        # Check if f(u) is a unit in S
        fu_inv = exquo(S, get_one(S), fu)
        
        # Check if u is a unit in R (if not, u^{-1} is undefined and conclusion fails)
        u_inv = exquo(R, get_one(R), u)
        
        # Check if f(u^{-1}) == f(u)^{-1}
        f_u_inv = apply_f(f, u_inv)
        
        conclusion = (f_u_inv == fu_inv)
    except Exception:
        # If any step fails (e.g., u is not a unit, so u^{-1} doesn't exist), the conclusion is False.
        conclusion = False

    neg_q = not conclusion

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f is a ring homomorphism",
    "H_3: f(1_R) = 1_S",
    "¬Q: f(u) is not a unit in S, or f(u^{-1}) != f(u)^{-1} (e.g., u is not a unit in R)"
]

N_HYP = 3
NEG_Q_INDEX = 3