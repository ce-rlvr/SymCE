import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

# Top-level setup for Ring Theory
Z = ZZ
Q = QQ
R = RR
C = CC

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: For every non-zero element x in K, either x in R or x^-1 in R",
    "¬Q: The ideals of R are not totally ordered by inclusion (R is not a valuation domain)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # 1. Dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = witness.get('is_integral_domain', witness.get('is_domain', False))
            h2 = witness.get('satisfies_valuation_property', witness.get('h2', False))
            q = witness.get('ideals_totally_ordered', witness.get('is_valuation_domain', True))
            return [bool(h1), bool(h2), not bool(q)]
        except Exception:
            pass

    # 2. Tuple witness (R, K)
    if isinstance(witness, tuple) and len(witness) == 2:
        R_ring, K_field = witness
        try:
            h1 = bool(getattr(R_ring, 'is_domain', False))
        except Exception:
            h1 = False
            
        try:
            # If K is exactly R, then for all x in K, x in R is trivially true.
            if K_field == R_ring:
                h2 = True
            elif hasattr(R_ring, 'fraction_field') and K_field == R_ring.fraction_field:
                h2 = bool(getattr(R_ring, 'is_Field', False))
            else:
                h2 = False
        except Exception:
            h2 = False
            
        try:
            # In SymPy, only fields have totally ordered ideals among standard commutative rings.
            q = bool(getattr(R_ring, 'is_Field', False))
        except Exception:
            q = False
            
        return [h1, h2, not q]

    # 3. Object witness (Mock object or single SymPy ring)
    h1 = False
    for attr in ['is_integral_domain', 'is_domain']:
        if hasattr(witness, attr):
            try:
                val = getattr(witness, attr)
                h1 = bool(val() if callable(val) else val)
                break
            except Exception:
                continue

    h2 = False
    for attr in ['satisfies_valuation_property', 'valuation_condition', 'is_valuation_ring', 'h2']:
        if hasattr(witness, attr):
            try:
                val = getattr(witness, attr)
                h2 = bool(val() if callable(val) else val)
                break
            except Exception:
                continue
    else:
        # Fallback for SymPy rings where K is implicitly the field of fractions
        if hasattr(witness, 'is_Field'):
            try:
                val = getattr(witness, 'is_Field')
                h2 = bool(val() if callable(val) else val)
            except Exception:
                pass

    q = True  # Default to True so neg_Q is False if not found
    for attr in ['ideals_totally_ordered', 'is_valuation_domain', 'totally_ordered_ideals', 'q']:
        if hasattr(witness, attr):
            try:
                val = getattr(witness, attr)
                q = bool(val() if callable(val) else val)
                break
            except Exception:
                continue
    else:
        # Fallback for SymPy rings
        if hasattr(witness, 'is_Field'):
            try:
                val = getattr(witness, 'is_Field')
                q = bool(val() if callable(val) else val)
            except Exception:
                pass

    return [h1, h2, not q]