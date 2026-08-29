import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.ntheory import factorint, isprime

# Top-level setup
# We define ZZ and QQ from sympy.polys.domains for use in witness expressions.
# A witness can be a SymPy domain, a tuple like ("localization", ZZ, p) or ("quotient", ZZ, n),
# or a custom object with properties/methods: is_commutative, is_local, prime_ideals_count.

def _is_commutative(ring):
    if hasattr(ring, 'is_commutative'):
        return ring.is_commutative() if callable(ring.is_commutative) else ring.is_commutative
    if ring in (ZZ, QQ):
        return True
    if isinstance(ring, tuple) and len(ring) == 3:
        op, base, arg = ring
        if op in ("localization", "quotient") and base == ZZ:
            return True
    return False

def _is_local(ring):
    if hasattr(ring, 'is_local'):
        return ring.is_local() if callable(ring.is_local) else ring.is_local
    if ring == QQ:
        return True
    if ring == ZZ:
        return False
    if isinstance(ring, tuple) and len(ring) == 3:
        op, base, arg = ring
        if op == "localization" and base == ZZ:
            try:
                return isprime(abs(int(arg)))
            except Exception:
                return False
        if op == "quotient" and base == ZZ:
            try:
                arg = abs(int(arg))
                if arg <= 1:
                    return False
                f = factorint(arg)
                return len(f) == 1
            except Exception:
                return False
    return False

def _prime_ideals_count(ring):
    if hasattr(ring, 'prime_ideals_count'):
        return ring.prime_ideals_count() if callable(ring.prime_ideals_count) else ring.prime_ideals_count
    if hasattr(ring, 'prime_ideals'):
        primes = ring.prime_ideals() if callable(ring.prime_ideals) else ring.prime_ideals
        return len(primes)
    if ring == QQ:
        return 1
    if ring == ZZ:
        return float('inf')
    if isinstance(ring, tuple) and len(ring) == 3:
        op, base, arg = ring
        if op == "localization" and base == ZZ:
            try:
                if isprime(abs(int(arg))):
                    return 2
            except Exception:
                pass
        if op == "quotient" and base == ZZ:
            try:
                arg = abs(int(arg))
                if arg <= 1:
                    return 0
                f = factorint(arg)
                return len(f)
            except Exception:
                pass
    return -1

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(_is_commutative(witness) and _is_local(witness))
    except Exception:
        h1 = False

    try:
        count = _prime_ideals_count(witness)
        neg_q = bool(count > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring with maximal ideal \\mathfrak{m}",
    "¬Q: \\mathfrak{m} is not the unique prime ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1