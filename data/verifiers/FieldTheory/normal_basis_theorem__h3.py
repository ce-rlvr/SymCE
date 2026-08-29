import sympy
from sympy import Poly, sympify, RootOf, factor_list
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups and matrices
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

def parse_witness(witness):
    """
    Parses the witness into a SymPy Poly object over the rationals.
    The witness is expected to be an irreducible polynomial defining the field extension K/Q.
    """
    if isinstance(witness, Poly):
        if witness.domain.is_QQ:
            return witness
        else:
            return Poly(witness.as_expr(), witness.gen, domain='QQ')
            
    if isinstance(witness, (tuple, list)):
        # If a tuple is provided, find the first element that is a valid expression with variables
        for item in witness:
            try:
                expr = sympify(item)
                if expr.free_symbols:
                    witness = expr
                    break
            except Exception:
                pass

    expr = sympify(witness)
    free = expr.free_symbols
    if len(free) == 1:
        var = list(free)[0]
    elif len(free) == 0:
        var = x
    else:
        var = list(free)[0]
        
    return Poly(expr, var, domain='QQ')

def conditions(witness) -> list[bool]:
    try:
        f_poly = parse_witness(witness)
        var = f_poly.gen
        f_expr = f_poly.as_expr()
    except Exception:
        return [False, False, False]
        
    # H_1: K is a field extension of F
    # We interpret the witness as the minimal polynomial of a primitive element of K over F=Q.
    try:
        h1 = bool(f_poly.degree() >= 1 and f_poly.is_irreducible)
    except Exception:
        h1 = False
        
    # H_2: The extension K/F is finite
    # Any polynomial extension is finite.
    try:
        h2 = bool(f_poly.degree() >= 1)
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist an element whose Galois orbit forms a basis for K over F.
    # This happens if and only if the extension is NOT Galois.
    # If it's not Galois, |Gal(K/F)| < [K:F], so no orbit can have enough elements to form a basis.
    try:
        if not h1:
            neg_q = False
        else:
            # Find one root to define the extension field K = Q(r)
            r = RootOf(f_expr, var, 0)
            # Factor the polynomial over K to find the number of roots in K
            factors = factor_list(f_expr, var, extension=r)[1]
            
            linear_factors = 0
            for fac, mult in factors:
                if Poly(fac, var).degree() == 1:
                    linear_factors += mult
                    
            # If the number of linear factors is less than the degree, it doesn't split completely,
            # meaning the extension is not Galois, and thus the conclusion fails.
            neg_q = bool(linear_factors < f_poly.degree())
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: The extension K/F is finite",
    "¬Q: No element's Galois orbit forms a basis for K over F"
]

N_HYP = 2
NEG_Q_INDEX = 2