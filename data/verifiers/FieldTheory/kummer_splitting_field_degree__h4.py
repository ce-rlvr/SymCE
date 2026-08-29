import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_finite_field(witness):
    try:
        n, p, P_coeffs = witness
    except Exception:
        return [False] * 4
        
    # H1: n is a positive integer
    try:
        h1 = int(n) == n and n > 0
    except Exception:
        h1 = False
        
    # H2: F is a field whose characteristic does not divide n
    try:
        h2 = sympy.isprime(p) and (n % p != 0)
    except Exception:
        h2 = False
        
    # H3: F contains all n-th roots of unity
    try:
        # F_p contains all n-th roots of unity iff n divides p-1
        h3 = sympy.isprime(p) and ((p - 1) % n == 0)
    except Exception:
        h3 = False
        
    # neg_Q: The splitting field of x^n - a over F does not have degree dividing n, 
    # or its Galois group is not cyclic.
    try:
        domain = sympy.GF(p)
        P_coeffs_clean = list(P_coeffs)
        # Strip leading zeros
        while len(P_coeffs_clean) > 1 and P_coeffs_clean[0] == 0:
            P_coeffs_clean = P_coeffs_clean[1:]
            
        P_y = sympy.Poly(P_coeffs_clean, x, domain=domain)
        
        # a must be a well-defined element of degree d over F_p
        if not P_y.is_irreducible:
            neg_q = False
        else:
            d = len(P_coeffs_clean) - 1
            poly_xn_coeffs = [0] * (d * n + 1)
            for i, c in enumerate(P_coeffs_clean):
                poly_xn_coeffs[n * i] = c
                
            P_xn = sympy.Poly(poly_xn_coeffs, x, domain=domain)
            factors = P_xn.factor_list()
            
            # The splitting field of P(x^n) over F_p has degree equal to the LCM 
            # of the degrees of its irreducible factors.
            deg = 1
            for factor, mult in factors[1]:
                deg = (deg * factor.degree()) // math.gcd(deg, factor.degree())
            
            # The Galois group of any finite extension of a finite field is cyclic.
            # Thus, the conclusion fails if and only if the degree does not divide n.
            neg_q = (n % deg != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

def check_number_field(witness):
    try:
        n, F_gen, a_expr = witness
    except Exception:
        return [False] * 4
        
    try:
        h1 = int(n) == n and n > 0
    except Exception:
        h1 = False
        
    try:
        h2 = True  # Number fields have characteristic 0, which never divides n > 0
    except Exception:
        h2 = False
        
    try:
        zeta = sympy.exp(2 * sympy.I * sympy.pi / n)
        minpoly_zeta = sympy.minimal_polynomial(zeta, x)
        if F_gen == 1:
            factors = sympy.factor_list(minpoly_zeta)
        else:
            factors = sympy.factor_list(minpoly_zeta, extension=F_gen)
        h3 = (factors[1][0][0].degree() == 1)
    except Exception:
        h3 = False
        
    try:
        root_a = a_expr ** (1 / n)
        minpoly_a = sympy.minimal_polynomial(root_a, x)
        if F_gen == 1:
            factors = sympy.factor_list(minpoly_a)
        else:
            factors = sympy.factor_list(minpoly_a, extension=F_gen)
            
        deg_a = factors[1][0][0].degree()
        neg_q = (n % deg_a != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

def conditions(witness):
    """
    Checks the witness against the hypotheses and the negated conclusion.
    Supports two witness formats:
      1. Finite field: (n, p, P_coeffs) where p is prime and P_coeffs defines a over F_p.
      2. Number field: (n, F_gen, a_expr) where F = Q(F_gen) and a_expr is a sympy expression.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            if isinstance(witness[2], list):
                return check_finite_field(witness)
            else:
                return check_number_field(witness)
    except Exception:
        pass
    return [False] * 4

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F is a field whose characteristic does not divide n",
    "H_3: F contains all n-th roots of unity",
    "¬Q: The splitting field of x^n - a over F does not have degree dividing n, or its Galois group is not cyclic"
]

N_HYP = 3
NEG_Q_INDEX = 3