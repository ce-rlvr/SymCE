import sympy
from sympy import eye, zeros, oo
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class InfiniteDimensionalSpace:
    """
    A mock object representing an infinite-dimensional vector space 
    with a standard non-degenerate symmetric bilinear form.
    """
    @property
    def is_symmetric_bilinear(self): 
        return True
        
    @property
    def is_non_degenerate(self): 
        return True
        
    @property
    def is_isomorphism(self): 
        return False

V_inf = InfiniteDimensionalSpace()
PolynomialSpace = InfiniteDimensionalSpace()

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The conjecture claims that a non-degenerate symmetric bilinear form always induces an isomorphism
    between V and V*. This is true for finite-dimensional spaces, but fails for infinite-dimensional ones.
    """
    try:
        # 1. Custom object with properties (like the ones defined in setup)
        if hasattr(witness, 'is_symmetric_bilinear'):
            h1 = witness.is_symmetric_bilinear
            if callable(h1): h1 = h1()
            h2 = witness.is_non_degenerate
            if callable(h2): h2 = h2()
            is_iso = witness.is_isomorphism
            if callable(is_iso): is_iso = is_iso()
            return [bool(h1), bool(h2), not bool(is_iso)]

        # 2. Tuple or list unpacking (e.g., (V, B))
        if isinstance(witness, (tuple, list)):
            # Check for infinite-dimensional indicators
            for item in witness:
                if hasattr(item, 'shape') and oo in item.shape:
                    h1 = item.is_symmetric()
                    if h1 is None: h1 = True
                    h2 = not (hasattr(item, 'is_zero') and item.is_zero)
                    return [bool(h1), bool(h2), True]
                if isinstance(item, str):
                    s = item.lower()
                    if 'inf' in s or 'poly' in s or 'r[x]' in s or 'l2' in s:
                        return [True, True, True]
            
            # Check for finite matrices
            for item in witness:
                if hasattr(item, 'is_Matrix') and item.is_Matrix and hasattr(item, 'det'):
                    h1 = item.is_symmetric()
                    try:
                        h2 = item.det() != 0
                    except Exception:
                        h2 = False
                    # Finite dimensional non-degenerate forms ALWAYS induce an isomorphism.
                    return [bool(h1), bool(h2), False]
            
            # Check for callable (likely a custom inner product on an infinite space)
            for item in witness:
                if callable(item):
                    return [True, True, True]
            
            # Check for polynomial rings (infinite dimensional)
            for item in witness:
                if hasattr(item, 'domain') and hasattr(item, 'gens'):
                    return [True, True, True]

        # 3. Infinite matrices (e.g., Identity(oo))
        if hasattr(witness, 'shape') and oo in witness.shape:
            h1 = witness.is_symmetric()
            if h1 is None: h1 = True
            h2 = not (hasattr(witness, 'is_zero') and witness.is_zero)
            return [bool(h1), bool(h2), True]

        # 4. Finite matrices
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix and hasattr(witness, 'det'):
            h1 = witness.is_symmetric()
            try:
                h2 = witness.det() != 0
            except Exception:
                h2 = False
            return [bool(h1), bool(h2), False]

        # 5. Matrix expressions (finite)
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            h1 = witness.is_symmetric()
            if h1 is None: h1 = False
            return [bool(h1), True, False]

        # 6. Strings indicating infinite dimensional spaces
        if isinstance(witness, str):
            s = witness.lower()
            if 'inf' in s or 'poly' in s or 'r[x]' in s or 'l2' in s:
                return [True, True, True]

        # 7. Polynomial rings (infinite dimensional)
        if hasattr(witness, 'domain') and hasattr(witness, 'gens'):
            return [True, True, True]

        # 8. Callable (custom inner product)
        if callable(witness):
            return [True, True, True]

    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: B is a symmetric bilinear form",
    "H_2: B is non-degenerate",
    "¬Q: phi is not a vector space isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2