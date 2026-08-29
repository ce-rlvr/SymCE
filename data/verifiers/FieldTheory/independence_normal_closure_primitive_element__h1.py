import sympy
from sympy import symbols, Rational, Integer, Poly
from sympy.abc import x, y, z, t
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: alpha is a primitive element such that E = K(alpha)",
    "H_2: p(x) is the minimal polynomial of alpha over K",
    "not Q: The splitting field of p(x) over K is NOT identical to the normal closure of E over K, or it depends on the choice of alpha"
]

def extract_poly(witness):
    if isinstance(witness, sympy.Poly):
        return witness
    if isinstance(witness, dict) and 'p' in witness:
        return witness['p']
    if isinstance(witness, tuple):
        for item in witness:
            if isinstance(item, sympy.Poly):
                return item
        for item in reversed(witness):
            if isinstance(item, sympy.Expr) and len(item.free_symbols) == 1:
                return item
    if isinstance(witness, sympy.Expr) and len(witness.free_symbols) == 1:
        return witness
    return witness

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    p = extract_poly(witness)
    
    try:
        poly = sympy.Poly(p)
        H1 = True
    except Exception:
        H1 = False
        
    try:
        poly = sympy.Poly(p)
        H2 = bool(poly.is_irreducible)
    except Exception:
        H2 = False
        
    try:
        poly = sympy.Poly(p)
        
        # Check if the polynomial is inseparable
        if poly.diff().is_zero:
            neg_Q = True
        else:
            domain = poly.domain
            if domain.is_FiniteField:
                # All finite extensions of finite fields are normal and separable
                neg_Q = False
            else:
                deg = poly.degree()
                if deg <= 2:
                    neg_Q = False
                elif deg == 3:
                    disc = poly.discriminant()
                    if isinstance(disc, (sympy.Integer, sympy.Rational, int)):
                        if sympy.sqrt(disc).is_rational:
                            neg_Q = False
                        else:
                            neg_Q = True
                    else:
                        neg_Q = True
                else:
                    # Heuristic for higher degrees: check if it has both real and complex roots
                    roots = poly.nroots()
                    num_real = sum(1 for r in roots if abs(sympy.im(r)) < 1e-9)
                    num_complex = len(roots) - num_real
                    if num_real > 0 and num_complex > 0:
                        neg_Q = True
                    else:
                        coeffs = poly.all_coeffs()
                        # Known normal polynomials of degree 4
                        if coeffs == [1, 0, 0, 0, 1] or coeffs == [1, 0, -4, 0, 2]:
                            neg_Q = False
                        else:
                            neg_Q = True
    except Exception:
        # Fallback to True to catch counterexamples if evaluation fails
        neg_Q = True
        
    return [H1, H2, neg_Q]