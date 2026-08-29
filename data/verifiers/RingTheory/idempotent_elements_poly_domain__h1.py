import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    if isinstance(witness, str):
        w = witness.strip().lower()
        if w in ["z", "zz", "q", "qq", "r", "c", "integers", "rationals", "reals"]:
            return [True, False]
        if "2z" in w or "even" in w or "rng" in w or "ideal" in w or "no identity" in w:
            return [True, True]
            
    if isinstance(witness, tuple) and len(witness) >= 2:
        if witness[0] == sympy.ZZ and witness[1] == 2:
            return [True, True]

    try:
        if witness in [sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes,
                       sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            return [True, False]
    except Exception:
        pass

    try:
        from sympy.polys.domains import Domain
        if isinstance(witness, Domain):
            h1 = True
            neg_q = False
    except Exception:
        pass

    try:
        if hasattr(witness, 'has_zero_divisors'):
            hz = witness.has_zero_divisors() if callable(witness.has_zero_divisors) else witness.has_zero_divisors
            h1 = not hz
        elif hasattr(witness, 'is_domain'):
            h1 = witness.is_domain
        elif hasattr(witness, 'zero_divisors'):
            zd = witness.zero_divisors() if callable(witness.zero_divisors) else witness.zero_divisors
            h1 = len(zd) == 0 or set(zd) == {0}
    except Exception:
        pass

    try:
        if hasattr(witness, 'idempotents'):
            idemps = witness.idempotents() if callable(witness.idempotents) else witness.idempotents
            neg_q = set(idemps) != {0, 1}
        elif hasattr(witness, 'has_identity'):
            hi = witness.has_identity() if callable(witness.has_identity) else witness.has_identity
            neg_q = not hi
        elif hasattr(witness, 'has_one'):
            neg_q = not witness.has_one
        elif hasattr(witness, 'one'):
            neg_q = witness.one is None
    except Exception:
        pass

    try:
        if hasattr(witness, 'ring') and hasattr(witness, 'contains'):
            ring = witness.ring
            if hasattr(ring, 'domain'):
                if getattr(ring.domain, 'is_Field', False) or ring.domain in [sympy.ZZ, sympy.QQ]:
                    h1 = True
            if hasattr(ring, 'one'):
                neg_q = not witness.contains(ring.one)
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R contains no non-zero zero divisors",
    "¬Q: The only idempotent elements in the polynomial ring are not just 0 and 1"
]

N_HYP = 1
NEG_Q_INDEX = 1