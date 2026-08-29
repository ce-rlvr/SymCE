import sympy
import sympy.polys
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def is_ring(ring):
    if hasattr(ring, 'is_Ring'):
        return ring.is_Ring() if callable(ring.is_Ring) else ring.is_Ring
    if hasattr(ring, 'is_ring'):
        return ring.is_ring() if callable(ring.is_ring) else ring.is_ring
    if hasattr(ring, 'is_integral_domain') or hasattr(ring, 'is_IntegralDomain'):
        return True
    from sympy.polys.domains import Domain
    if isinstance(ring, Domain):
        return True
    if type(ring).__name__ in ('PolyRing', 'QuotientRing'):
        return True
    return False

def is_integral_domain(ring):
    if hasattr(ring, 'is_integral_domain'):
        return ring.is_integral_domain() if callable(ring.is_integral_domain) else ring.is_integral_domain
    if hasattr(ring, 'is_IntegralDomain'):
        return ring.is_IntegralDomain() if callable(ring.is_IntegralDomain) else ring.is_IntegralDomain
    if hasattr(ring, 'is_domain'):
        return ring.is_domain() if callable(ring.is_domain) else ring.is_domain
    
    if type(ring).__name__ == 'QuotientRing':
        try:
            return ring.base_ideal.is_prime()
        except Exception:
            return False
            
    from sympy.polys.domains import Domain
    if isinstance(ring, Domain):
        return True
    if type(ring).__name__ == 'PolyRing':
        return True
        
    return False

def is_field(F):
    if hasattr(F, 'is_Field'):
        return F.is_Field() if callable(F.is_Field) else F.is_Field
    if hasattr(F, 'is_field'):
        return F.is_field() if callable(F.is_field) else F.is_field
    if hasattr(F, 'get_field'):
        try:
            return F.get_field() == F
        except Exception:
            pass
    return False

def is_field_of_fractions(K, R):
    if hasattr(R, 'get_field'):
        try:
            if R.get_field() == K:
                return True
        except Exception:
            pass
    if hasattr(R, 'fraction_field'):
        try:
            frac = R.fraction_field() if callable(R.fraction_field) else R.fraction_field
            if frac == K:
                return True
        except Exception:
            pass
    if hasattr(R, 'field_of_fractions'):
        try:
            frac = R.field_of_fractions() if callable(R.field_of_fractions) else R.field_of_fractions
            if frac == K:
                return True
        except Exception:
            pass
    return False

def is_field_extension(L, K):
    if not is_field(L):
        return False
    if not is_field(K):
        return False
    if L == K:
        return True
    if hasattr(K, 'unify'):
        try:
            if K.unify(L) == L:
                return True
        except Exception:
            pass
    if hasattr(L, 'is_extension_of'):
        try:
            if L.is_extension_of(K):
                return True
        except Exception:
            pass
    if hasattr(L, 'domain'):
        try:
            if L.domain == K:
                return True
        except Exception:
            pass
    if hasattr(L, 'has_subring'):
        try:
            if L.has_subring(K):
                return True
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            L = witness.get('L')
            S = witness.get('S')
        else:
            if len(witness) != 4:
                return [False, False, False, False]
            R, K, L, S = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_integral_domain(R)
    except Exception:
        h1 = False

    try:
        h2 = is_field_of_fractions(K, R)
    except Exception:
        h2 = False

    try:
        h3 = is_field_extension(L, K)
    except Exception:
        h3 = False

    try:
        neg_q = is_ring(S) and not is_integral_domain(S)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: L is a field extension of K",
    "¬Q: S is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3