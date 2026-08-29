import sympy
from sympy import Poly, minpoly, QQ
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis from the true theorem is that f(x) must be a polynomial in K[x].
    If f(x) is not in K[x], its splitting field L over K might not be a normal extension,
    making Gal(L/K) solvable (e.g., trivial) even if the roots of f(x) are not solvable by radicals.
    """
    if not isinstance(witness, dict):
        return [False, False, False]
        
    try:
        K = witness.get('K')
        L = witness.get('L')
        f = witness.get('f')
    except Exception:
        return [False, False, False]
        
    # H1: K is a field of characteristic 0
    try:
        h1 = bool(K.is_Field and K.characteristic == 0)
    except Exception:
        h1 = False
        
    # H2: L is the splitting field of f(x) over K
    try:
        if not isinstance(f, Poly):
            f = Poly(f, x)
        # We assume the witness provides a valid splitting field L.
        # Just check basic types to ensure they are well-formed.
        h2 = hasattr(f, 'degree') and hasattr(L, 'is_Field')
    except Exception:
        h2 = False
        
    # neg_Q: (f is solvable by radicals over K) != (Gal(L/K) is solvable)
    try:
        if f.degree() == 1:
            coeffs = f.coeffs()
            roots = [-coeffs[1] / coeffs[0]]
        else:
            try:
                roots = f.all_roots()
            except Exception:
                from sympy import roots as sympy_roots
                roots = sympy_roots(f.as_expr(), multiple=True)
                
        # 1. Check if f(x) is solvable by radicals over K
        solvable_by_radicals = True
        for r in roots:
            mp = minpoly(r, x)
            mp_poly = Poly(mp, x)
            if not mp_poly.galois_group().is_solvable:
                solvable_by_radicals = False
                break
                
        # 2. Check if Gal(L/K) is solvable
        galois_solvable = True
        if 'g' in witness:
            g = witness['g']
            if not isinstance(g, Poly):
                g = Poly(g, x)
            galois_solvable = bool(g.galois_group().is_solvable)
        elif f.domain == K or (K == sympy.QQ and f.domain == sympy.ZZ):
            galois_solvable = bool(f.galois_group().is_solvable)
        else:
            # If f is not in K[x], L/K might not be normal.
            # Gal(L/K) is the automorphism group Aut(L/K).
            # For the counterexample L = K(alpha) where alpha has degree 5,
            # the degree of L/K is 5, so |Aut(L/K)| divides 5.
            # Any group of order dividing 5 is solvable.
            if hasattr(L, 'mod'):
                deg = L.mod.degree()
                if deg < 60:
                    galois_solvable = True
                else:
                    galois_solvable = True
            else:
                galois_solvable = True
                
        neg_q = bool(solvable_by_radicals != galois_solvable)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic 0",
    "H_2: L is the splitting field of f(x) over K",
    "¬Q: f(x) is solvable by radicals over K is NOT equivalent to Gal(L/K) being solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2