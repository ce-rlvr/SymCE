import sympy
from sympy.polys.domains import ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not natively implement non-UFD domains like Z[sqrt(-5)], 
# we provide mock objects representing these standard counterexamples.
class _CustomRing:
    def __init__(self, name, is_integral_domain, is_ufd, is_field=False):
        self.name = name
        self.is_IntegralDomain = is_integral_domain
        self.is_UFD = is_ufd
        self.is_Field = is_field
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.name

Z_sqrt_minus_5 = _CustomRing("Z[sqrt(-5)]", True, False, False)
Z_sqrt_minus_3 = _CustomRing("Z[sqrt(-3)]", True, False, False)

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        if hasattr(witness, 'is_IntegralDomain'):
            h1 = bool(witness.is_IntegralDomain)
        elif hasattr(witness, 'is_UFD') and hasattr(witness, 'is_Field'):
            # Standard SymPy domains (ZZ, QQ, ZZ[x], etc.) are all integral domains
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: R is not a unique factorization domain
    try:
        if hasattr(witness, 'is_Field') and witness.is_Field:
            # Every field is mathematically a UFD. (Overrides SymPy's EX.is_UFD = False limitation)
            neg_q = False
        elif hasattr(witness, 'is_UFD'):
            neg_q = not bool(witness.is_UFD)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 1
NEG_Q_INDEX = 1