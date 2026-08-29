import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.domains import Domain

# Top-level setup
Z = ZZ
Q = QQ
Z_x = ZZ.old_poly_ring(x)
Q_x = QQ.old_poly_ring(x)
Z_x_y = ZZ.old_poly_ring(x, y)
Q_x_y = QQ.old_poly_ring(x, y)

def is_dedekind_domain(D):
    """
    Checks if a SymPy domain is a Dedekind domain.
    A Dedekind domain is an integral domain that is Noetherian, integrally closed,
    and has Krull dimension at most 1.
    """
    if getattr(D, 'is_Field', False):
        return True
    if D == ZZ:
        return True
    
    domain = getattr(D, 'domain', None)
    if domain is not None:
        gens = getattr(D, 'gens', getattr(D, 'symbols', None))
        if gens is not None:
            # A polynomial ring over a field with exactly 1 generator is a PID,
            # and therefore a Dedekind domain.
            if len(gens) == 1 and getattr(domain, 'is_Field', False):
                return True
            # Polynomial rings with >1 generator or over non-fields (like ZZ[x])
            # have dimension >= 2, so they are not Dedekind domains.
            return False
            
    return False

def conditions(witness) -> list[bool]:
    try:
        # The witness must be a valid SymPy domain (ring)
        if not isinstance(witness, Domain):
            return [False]
            
        # The negated conclusion is True if the ring is NOT a Dedekind domain
        neg_q = not is_dedekind_domain(witness)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Dedekind domain"
]

N_HYP = 0
NEG_Q_INDEX = 0