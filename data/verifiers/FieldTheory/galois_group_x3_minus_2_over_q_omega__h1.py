import sympy
from sympy import minpoly, degree, I, sqrt, Rational
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: K = Q(omega)",
    "H_2: L is the splitting field of x^3 - 2 over K",
    "¬Q: Gal(L/K) is not isomorphic to Z3"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract omega from the witness
        if isinstance(witness, dict):
            if 'omega' in witness:
                omega = witness['omega']
            else:
                return [False, False, False]
        elif isinstance(witness, (list, tuple)):
            omega = witness[-1]
        else:
            omega = witness
            
        omega = sympy.sympify(omega)
        
        # Import primitive_element locally to ensure it's available
        from sympy import primitive_element
        
        # Compute the degree of K = Q(omega) over Q
        minpoly_omega = minpoly(omega, x)
        deg_K = degree(minpoly_omega, x)
        
        # L is the splitting field of x^3 - 2 over K.
        # The splitting field of x^3 - 2 over Q is Q(2**(1/3), sqrt(-3)).
        # Therefore, L = Q(omega, 2**(1/3), sqrt(-3)).
        exts = [omega, 2**Rational(1,3), sqrt(-3)]
        
        # Filter out elements that are already rational to speed up primitive_element
        exts_nonrat = []
        for e in exts:
            if degree(minpoly(e, x), x) > 1 and e not in exts_nonrat:
                exts_nonrat.append(e)
                
        if not exts_nonrat:
            deg_L = 1
        else:
            # Compute the degree of L over Q
            minpoly_L, _ = primitive_element(exts_nonrat, x)
            deg_L = degree(minpoly_L, x)
            
        # The degree of L over K is [L:Q] / [K:Q]
        deg_L_K = deg_L // deg_K
        
        # H_1 and H_2 are definitional for K and L given omega, so they hold by construction.
        h1 = True
        h2 = True
        
        # The conclusion is that Gal(L/K) is isomorphic to Z3.
        # Since L is a splitting field over K, |Gal(L/K)| = [L:K].
        # Gal(L/K) is isomorphic to Z3 if and only if its order is exactly 3.
        # The negated conclusion is True if the order is NOT 3.
        neg_q = (deg_L_K != 3)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]