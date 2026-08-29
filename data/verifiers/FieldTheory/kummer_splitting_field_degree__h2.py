import sympy
from sympy import Symbol, Poly, QQ, GF
from sympy.abc import x, t, u, v
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    The witness should be a tuple: (n, F, a)
    where n is an integer, F is a SymPy field domain, and a is an element of F.
    """
    try:
        n, F, a = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    # H_2: F contains all n-th roots of unity
    # This is true if and only if x^n - 1 splits completely into linear factors over F.
    try:
        if hasattr(F, 'is_Field') and F.is_Field:
            poly_1 = Poly(x**n - 1, x, domain=F)
            factors_1 = poly_1.factor_list()[1]
            h2 = all(fac.degree() == 1 for fac, mult in factors_1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: a in F is a non-zero element
    try:
        a_val = F(a)
        h3 = (a_val != F.zero)
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails
    # The conclusion states that the splitting field has degree dividing n and its Galois group is cyclic.
    # By Kummer theory, if F contains all n-th roots of unity, this conclusion holds IF AND ONLY IF 
    # the extension is separable (i.e., it is a Galois extension). 
    # The conclusion fails exactly when the characteristic p divides n and 'a' is chosen such that 
    # x^n - a has inseparable irreducible factors, meaning the splitting field is not a Galois extension.
    try:
        poly_a = Poly(x**n - a, x, domain=F)
        factors_a = poly_a.factor_list()[1]
        
        # Check if all irreducible factors are separable (gcd with derivative is degree 0)
        is_separable = True
        for fac, mult in factors_a:
            derivative = fac.diff(x)
            if fac.gcd(derivative).degree() > 0:
                is_separable = False
                break
                
        neg_q = not is_separable
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F contains all n-th roots of unity",
    "H_3: a in F is a non-zero element",
    "¬Q: The splitting field of x^n - a over F is not a Galois extension (or degree does not divide n, or Galois group is not cyclic)"
]

N_HYP = 3
NEG_Q_INDEX = 3