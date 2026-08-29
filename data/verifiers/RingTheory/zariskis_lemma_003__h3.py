import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ, GF

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (k, E) where k is the base field and E is the k-algebra.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        k, E = witness
    except Exception:
        return [False, False, False]
    
    # H_1: k is a field
    try:
        h1_ok = bool(getattr(k, 'is_Field', False))
    except Exception:
        h1_ok = False
        
    # H_2: E is a finitely generated k-algebra
    try:
        h2_ok = False
        if E == k:
            h2_ok = True
        else:
            is_poly = getattr(E, 'is_PolyRing', False) or getattr(E, 'is_PolynomialRing', False)
            is_alg = getattr(E, 'is_AlgebraicField', False)
            base = getattr(E, 'domain', None)
            
            if is_poly and base == k:
                h2_ok = True
            elif is_alg and base == k:
                h2_ok = True
            elif hasattr(E, 'base_ring'):
                base_ring = E.base_ring
                is_base_poly = getattr(base_ring, 'is_PolyRing', False) or getattr(base_ring, 'is_PolynomialRing', False)
                if is_base_poly and getattr(base_ring, 'domain', None) == k:
                    h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: E is NOT a finite algebraic extension of k
    try:
        q = False
        if E == k:
            q = True
        elif getattr(E, 'is_AlgebraicField', False) and getattr(E, 'domain', None) == k:
            q = True
        elif getattr(E, 'is_Field', False):
            # By Zariski's Lemma, a finitely generated k-algebra is a finite algebraic extension iff it is a field.
            q = True
        else:
            q = False
            
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: E is a finitely generated k-algebra",
    "¬Q: E is not a finite algebraic extension of k"
]

N_HYP = 2
NEG_Q_INDEX = 2