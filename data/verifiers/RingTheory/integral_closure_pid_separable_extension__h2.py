import sympy
from sympy.polys.domains import ZZ, QQ
from sympy import Symbol

class InfiniteAlgebraicExtension:
    """Represents an infinite algebraic extension of a base field."""
    def __init__(self, base_field):
        self.base_field = base_field
        
    def __eq__(self, other):
        if not isinstance(other, InfiniteAlgebraicExtension):
            return False
        return self.base_field == other.base_field

class IntegralClosure:
    """Represents the integral closure of a base ring in an extension field."""
    def __init__(self, base_ring, extension_field):
        self.base_ring = base_ring
        self.extension_field = extension_field
        
    def __eq__(self, other):
        if not isinstance(other, IntegralClosure):
            return False
        return self.base_ring == other.base_ring and self.extension_field == other.extension_field

# Standard counterexample objects for the missing 'finite extension' hypothesis
QQ_bar = InfiniteAlgebraicExtension(QQ)
Z_bar = IntegralClosure(ZZ, QQ_bar)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            L = witness.get('L')
            S = witness.get('S')
            if any(x is None for x in (R, K, L, S)):
                return [False, False, False]
        else:
            if len(witness) != 4:
                return [False, False, False]
            R, K, L, S = witness
    except Exception:
        return [False, False, False]

    # H1: R is a principal ideal domain with field of fractions K
    try:
        h1 = False
        if R == ZZ and K == QQ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            if hasattr(R, 'get_field') and K == R.get_field():
                h1 = True
            elif hasattr(R, 'frac_field') and K == R.frac_field():
                h1 = True
    except Exception:
        h1 = False

    # H2: S is the integral closure of R in L
    try:
        h2 = False
        if isinstance(S, IntegralClosure) and S.base_ring == R and S.extension_field == L:
            h2 = True
        elif L == K and S == R:
            h2 = True
        elif hasattr(K, 'frac_field') and hasattr(L, 'symbols'):
            if L == K.frac_field(*L.symbols) and S == R:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: S is not a Dedekind domain
    try:
        neg_q = False
        if isinstance(S, IntegralClosure):
            if isinstance(S.extension_field, InfiniteAlgebraicExtension):
                neg_q = True
        elif S == ZZ:
            neg_q = False
        elif hasattr(S, 'is_PID') and S.is_PID:
            neg_q = False
        elif hasattr(S, 'domain') and S.domain == ZZ and len(getattr(S, 'symbols', [])) >= 1:
            neg_q = True
        elif hasattr(S, 'domain') and S.domain.is_Field and len(getattr(S, 'symbols', [])) >= 2:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain with field of fractions K",
    "H_2: S is the integral closure of R in L",
    "¬Q: S is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2