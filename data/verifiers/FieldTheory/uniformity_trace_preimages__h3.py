import sympy
from sympy import Poly
from sympy.abc import x
from sympy.polys.domains import FF, ZZ
from sympy.ntheory import factorint
import itertools
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_irreducible_poly(p, deg):
    """Finds an irreducible polynomial of degree `deg` over F_p."""
    try:
        from sympy.polys.galoistools import gf_irreducible
        res = gf_irreducible(deg, p, ZZ)
        if res:
            return res
    except Exception:
        pass
        
    # Fallback for small fields if gf_irreducible is unavailable
    if p**deg > 100000:
        raise ValueError("p**deg too large for fallback irreducible polynomial generation")
        
    for coeffs in itertools.product(range(p), repeat=deg):
        poly_coeffs = [1] + list(coeffs)
        P = Poly(poly_coeffs, x, domain=FF(p))
        if P.is_irreducible:
            return poly_coeffs
    return None

def poly_pow_mod(base, exp, mod_poly):
    """Computes (base^exp) % mod_poly efficiently."""
    res = Poly([1], x, domain=base.domain)
    base = base % mod_poly
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod_poly
        base = (base * base) % mod_poly
        exp //= 2
    return res

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (q, n, c)
    where c is an element of F_{q^n} (represented as an int, list of coeffs, or Poly).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        q, n, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F_q is a finite field with q elements (q must be a prime power)
    try:
        if isinstance(q, int) and q >= 2:
            factors = factorint(q)
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: F_{q^n} is a finite field extension of F_q of degree n
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False
        
    # ¬Q: The number of elements x in F_{q^n} such that Tr(x) = c is NOT exactly q^{n-1}
    # Mathematically, the trace map Tr: F_{q^n} -> F_q is surjective.
    # Thus, if c in F_q, the number of preimages is exactly q^{n-1}.
    # If c not in F_q, the number of preimages is 0 (which is != q^{n-1} since q>=2, n>=1).
    # Therefore, the conclusion fails iff c is NOT in F_q.
    # We check if c in F_q by testing if c^q == c in F_{q^n}.
    try:
        neg_q = False
        if h1 and h2:
            factors = factorint(q)
            p = list(factors.keys())[0]
            k = factors[p]
            deg = k * n
            
            poly_coeffs = get_irreducible_poly(p, deg)
            if poly_coeffs:
                mod_poly = Poly(poly_coeffs, x, domain=FF(p))
                
                if isinstance(c, int):
                    c_poly = Poly([c % p], x, domain=FF(p))
                elif isinstance(c, (list, tuple)):
                    c_poly = Poly([val % p for val in c], x, domain=FF(p))
                else:
                    try:
                        c_poly = Poly(c, x, domain=FF(p))
                    except Exception:
                        c_poly = None
                        
                if c_poly is not None:
                    c_poly = c_poly % mod_poly
                    c_q = poly_pow_mod(c_poly, q, mod_poly)
                    
                    # If c^q != c, then c is not in F_q, so it has 0 preimages (!= q^{n-1})
                    neg_q = (c_q != c_poly)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^n} is a finite field extension of F_q of degree n",
    "¬Q: The number of elements x in F_{q^n} such that Tr(x) = c is not exactly q^{n-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2