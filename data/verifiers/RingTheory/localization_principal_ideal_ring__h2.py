import sympy
import sympy.combinatorics
import sympy.matrices
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative ring and S is a multiplicatively closed subset of R,
    then the localized ring S^{-1}R is a principal ideal ring."
    
    A valid witness is a tuple (R, S) where R is a SymPy domain or PolyRing,
    and S is a finite list/set/tuple of elements generating the multiplicatively
    closed subset.
    """
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring
    try:
        from sympy.polys.domains.domain import Domain
        # SymPy Domains and PolyRings are commutative rings
        h1 = isinstance(R, Domain) or type(R).__name__ in ('PolyRing', 'QuotientRing')
    except Exception:
        h1 = False
        
    # H_2: S is a multiplicatively closed subset of R
    try:
        if not isinstance(S, (list, set, tuple)):
            h2 = False
        elif len(S) > 100:
            # Restrict size to ensure fast evaluation
            h2 = False
        else:
            S_list = list(S)
            h2 = True
            # Check that all elements belong to R
            for a in S_list:
                try:
                    _ = R(a)
                except Exception:
                    h2 = False
                    break
            # Check closure under multiplication
            if h2:
                for a in S_list:
                    for b in S_list:
                        prod = R(a) * R(b)
                        if not any(prod == R(s) for s in S_list):
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # ¬Q: S^{-1}R is NOT a principal ideal ring
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            # If 0 is in S, S^{-1}R is the zero ring, which is a PIR.
            if any(R(s) == getattr(R, 'zero', 0) for s in S_list):
                is_pir = True
            else:
                # Since S is finite and multiplicatively closed, and 0 not in S,
                # S must consist entirely of units (roots of unity).
                # Thus, S^{-1}R is isomorphic to R. We just check if R is a PIR.
                if getattr(R, 'is_Field', False):
                    is_pir = True
                elif getattr(R, 'name', '') == 'ZZ':
                    is_pir = True
                elif hasattr(R, 'dom') and hasattr(R, 'symbols'):
                    base = R.dom
                    gens = R.symbols
                    # K[x] is a PIR iff K is a field and there is at most 1 generator
                    if getattr(base, 'is_Field', False) and len(gens) <= 1:
                        is_pir = True
                    else:
                        is_pir = False
                elif hasattr(R, 'domain') and hasattr(R, 'gens'):
                    base = R.domain
                    gens = R.gens
                    if getattr(base, 'is_Field', False) and len(gens) <= 1:
                        is_pir = True
                    else:
                        is_pir = False
                else:
                    # Default fallback
                    is_pir = getattr(R, 'is_Field', False)
            
            neg_q = not is_pir
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: S^{-1}R is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2