import sympy

# Top-level setup: named object bindings that the witness expression may reference.
# Integers n >= 1 represent the ring Z_n (integers modulo n).
# Z_1 is the zero ring.
Z1 = 1
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
ZZ = sympy.ZZ
QQ = sympy.QQ

def _is_comm_ring_with_id(R):
    if type(R) is int and R >= 1:
        return True
    if R in (sympy.ZZ, sympy.QQ):
        return True
    return False

def _is_zero_ring(R):
    if type(R) is int:
        return R == 1
    if R in (sympy.ZZ, sympy.QQ):
        return False
    return False

def _is_integral_domain(R):
    if type(R) is int:
        return sympy.isprime(R)
    if R in (sympy.ZZ, sympy.QQ):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        R, S = witness
    except Exception:
        return [False, False, False]

    # H_1: R and S are commutative rings with identity
    try:
        h1 = _is_comm_ring_with_id(R) and _is_comm_ring_with_id(S)
    except Exception:
        h1 = False

    # H_2: S is not the zero ring
    try:
        h2 = _is_comm_ring_with_id(S) and not _is_zero_ring(S)
    except Exception:
        h2 = False

    # ¬Q: R \times S is an integral domain
    # The direct product of two rings is an integral domain if and only if 
    # one is the zero ring and the other is an integral domain.
    try:
        r_zero = _is_zero_ring(R)
        s_zero = _is_zero_ring(S)
        
        if r_zero and s_zero:
            neg_q = False
        elif r_zero:
            neg_q = _is_integral_domain(S)
        elif s_zero:
            neg_q = _is_integral_domain(R)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: S is not the zero ring",
    "¬Q: R x S is an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2