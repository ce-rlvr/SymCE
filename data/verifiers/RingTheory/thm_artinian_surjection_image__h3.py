import sympy
from sympy import ZZ, QQ
from sympy.abc import x

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture:
    "If R and S are rings and f: R -> S is a surjective ring homomorphism, then S is an Artinian ring."
    
    A valid witness should be a tuple (R, S, f) where:
      - R and S are rings (e.g., sympy.ZZ, sympy.QQ, or custom objects)
      - f is a callable representing a surjective ring homomorphism from R to S
    """
    try:
        R, S, f = witness
    except Exception:
        return [False, False, False]
    
    if isinstance(f, dict):
        f_map = f
        f = lambda val: f_map[val]

    # H_1: R and S are rings
    try:
        def check_ring(ring):
            if hasattr(ring, 'is_ring'):
                val = ring.is_ring
                if callable(val): return val()
                return val
            return hasattr(ring, 'zero') and hasattr(ring, 'one')
        
        h1 = bool(check_ring(R) and check_ring(S))
    except Exception:
        h1 = False

    # H_2: f is a surjective ring homomorphism
    try:
        def get_test_elements(ring):
            if hasattr(ring, 'elements'):
                val = ring.elements
                return val() if callable(val) else list(val)
            if ring == ZZ:
                return [ZZ(i) for i in range(-15, 16)]
            if ring == QQ:
                from sympy import Rational
                return [Rational(i, j) for i in range(-3, 4) for j in range(1, 4)]
            if hasattr(ring, 'gens') and len(ring.gens) > 0:
                g = ring.gens[0]
                return [ring.zero, ring.one, g, g + ring.one, g**2]
            return [ring.zero, ring.one]
        
        elems_R = get_test_elements(R)
        elems_S = get_test_elements(S)
        
        is_hom = True
        if not (f(R.one) == S.one):
            is_hom = False
        else:
            for a in elems_R:
                for b in elems_R:
                    if not (f(a + b) == f(a) + f(b)):
                        is_hom = False
                        break
                    if not (f(a * b) == f(a) * f(b)):
                        is_hom = False
                        break
                if not is_hom:
                    break
        
        is_surj = True
        if is_hom:
            if hasattr(R, 'elements'):
                val = R.elements
                large_elems_R = val() if callable(val) else list(val)
            elif R == ZZ:
                large_elems_R = [ZZ(i) for i in range(-100, 101)]
            else:
                large_elems_R = elems_R
            
            images = []
            for r in large_elems_R:
                try:
                    images.append(f(r))
                except Exception:
                    pass
            
            for s in elems_S:
                if s not in images:
                    is_surj = False
                    break
                    
        h2 = bool(is_hom and is_surj)
    except Exception:
        h2 = False

    # neg_Q: S is not an Artinian ring
    try:
        def is_artinian(ring):
            if hasattr(ring, 'is_artinian'):
                val = ring.is_artinian
                return val() if callable(val) else val
            if ring == ZZ:
                return False
            if getattr(ring, 'is_Field', False):
                return True
            if hasattr(ring, 'gens'):
                return False
            return True
            
        neg_q = not is_artinian(S)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "¬Q: S is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2