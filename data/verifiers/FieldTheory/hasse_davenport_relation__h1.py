import sympy
from sympy import I, exp, pi, primitive_root, isprime, simplify
from sympy.polys.galoistools import gf_irreducible, gf_pow, gf_mul, gf_rem, gf_add
from sympy.polys.domains import ZZ
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential named objects
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

def compute_gauss_sums(p, n, d):
    g = primitive_root(p)
    dlog = {pow(g, k, p): k for k in range(p - 1)}
    
    # Compute g(chi) over F = F_p
    g_chi = 0
    for k in range(p - 1):
        x = pow(g, k, p)
        chi_x = exp(2 * pi * I * k / d)
        psi_x = exp(2 * pi * I * x / p)
        g_chi += chi_x * psi_x
    g_chi = simplify(g_chi)
    
    # Compute g(chi') over E = F_{p^n}
    irr = gf_irreducible(n, p, ZZ)
    elements = list(itertools.product(range(p), repeat=n))
    g_chi_prime = 0
    
    for coeffs in elements:
        poly = list(coeffs)
        while poly and poly[0] == 0:
            poly.pop(0)
        if not poly:
            continue
            
        cur = poly
        norm = poly
        trace = poly
        for _ in range(n - 1):
            cur = gf_pow(cur, p, irr, p, ZZ)
            norm = gf_mul(norm, cur, p, ZZ)
            norm = gf_rem(norm, irr, p, ZZ)
            trace = gf_add(trace, cur, p, ZZ)
            
        n_val = norm[-1] if norm else 0
        t_val = trace[-1] if trace else 0
        
        if n_val == 0:
            continue
            
        k = dlog[n_val]
        chi_x = exp(2 * pi * I * k / d)
        psi_x = exp(2 * pi * I * t_val / p)
        g_chi_prime += chi_x * psi_x
        
    g_chi_prime = simplify(g_chi_prime)
    return g_chi, g_chi_prime

def conditions(witness) -> list[bool]:
    # Try to evaluate as a mock object first
    try:
        if hasattr(witness, "is_finite_field_extension"):
            h1 = bool(witness.is_finite_field_extension)
            h2 = bool(witness.chi_is_non_trivial)
            h3 = bool(witness.chi_prime_is_lifted)
            h4 = bool(witness.gauss_sums_are_canonical)
            if hasattr(witness, "conclusion_holds"):
                neg_q = not bool(witness.conclusion_holds)
            else:
                neg_q = True
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # Try to evaluate as a dictionary
    try:
        if isinstance(witness, dict) and "is_finite_field_extension" in witness:
            h1 = bool(witness.get("is_finite_field_extension", False))
            h2 = bool(witness.get("chi_is_non_trivial", False))
            h3 = bool(witness.get("chi_prime_is_lifted", False))
            h4 = bool(witness.get("gauss_sums_are_canonical", False))
            neg_q = not bool(witness.get("conclusion_holds", True))
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # Try to evaluate as a tuple representing (p, n, d)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            p, n, d = witness
            h1 = isprime(p) and n >= 1
            h2 = d > 1 and (p - 1) % d == 0
            h3 = True
            h4 = True
            
            if h1 and h2:
                g_chi, g_chi_prime = compute_gauss_sums(p, n, d)
                lhs = simplify(-g_chi_prime)
                rhs = simplify((-g_chi)**n)
                neg_q = bool(lhs != rhs)
            else:
                neg_q = False
                
            return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass
        
    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: E is a finite field extension of F of degree n",
    "H_2: chi is a non-trivial multiplicative character of F",
    "H_3: chi' is the lifted multiplicative character on E defined by chi' = chi o N_{E/F}",
    "H_4: g(chi) and g(chi') are the Gauss sums of chi and chi' with respect to the canonical additive characters of F and E",
    "¬Q: -g(chi') != (-g(chi))^n"
]

N_HYP = 4
NEG_Q_INDEX = 4