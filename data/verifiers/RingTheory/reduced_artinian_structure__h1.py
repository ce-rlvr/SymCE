import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

# Top-level setup for Ring Theory
# The standard domains ZZ, QQ, RR, CC and variables x, y, z are available.

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "A reduced ring is isomorphic to a finite direct product of division rings."
    """
    
    # Helper to map SymPy sets to SymPy domains if necessary
    def normalize(w):
        if w == sympy.S.Integers: return ZZ
        if w == sympy.S.Rationals: return QQ
        if w == sympy.S.Reals: return RR
        if w == sympy.S.Complexes: return CC
        return w

    try:
        if isinstance(witness, tuple):
            norm_witness = tuple(normalize(w) for w in witness)
        else:
            norm_witness = normalize(witness)
    except Exception:
        norm_witness = witness

    def is_reduced(w):
        # A tuple of rings is reduced if all components are reduced.
        if isinstance(w, tuple):
            return all(is_reduced(part) for part in w)
        # In SymPy, integral domains and fields have no non-zero nilpotent elements.
        return bool(getattr(w, 'is_IntegralDomain', False) or getattr(w, 'is_Field', False))

    def is_prod_div_rings(w):
        # A tuple of rings is a product of division rings if all components are division rings.
        if isinstance(w, tuple):
            return all(is_prod_div_rings(part) for part in w)
        # For commutative domains in SymPy, a division ring is a field.
        return bool(getattr(w, 'is_Field', False))

    try:
        # H_1: R is a reduced ring
        h1 = is_reduced(norm_witness)
    except Exception:
        h1 = False

    try:
        # ¬Q: R is NOT isomorphic to a finite direct product of division rings
        # If R is an integral domain, it has no zero divisors.
        # A finite direct product of division rings has zero divisors unless it consists of exactly one division ring.
        # Thus, an integral domain is a finite direct product of division rings iff it is a division ring (field).
        if h1:
            neg_q = not is_prod_div_rings(norm_witness)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "¬Q: R is not isomorphic to a finite direct product of division rings"
]

N_HYP = 1
NEG_Q_INDEX = 1