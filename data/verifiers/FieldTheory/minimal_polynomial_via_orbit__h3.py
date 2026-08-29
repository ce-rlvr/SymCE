import sympy as sp
from sympy import Poly
from sympy.abc import x, y, z, t

# Standard algebra objects
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

from sympy.matrices import eye, zeros
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    witness is expected to be a dictionary or a 3-tuple:
    {
        'theta_minpoly': expr in t (minimal polynomial of primitive element theta over QQ),
        'automorphisms': list of expr in t (images of theta under the Galois group),
        'alpha_expr': expr in t (alpha as an element of QQ(theta))
    }
    """
    try:
        if isinstance(witness, dict):
            theta_minpoly = sp.sympify(witness.get('theta_minpoly'))
            automorphisms = [sp.sympify(a) for a in witness.get('automorphisms', [])]
            alpha_expr = sp.sympify(witness.get('alpha_expr'))
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            theta_minpoly = sp.sympify(witness[0])
            automorphisms = [sp.sympify(a) for a in witness[1]]
            alpha_expr = sp.sympify(witness[2])
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: L/K is a finite Galois extension of fields with Galois group G
    try:
        p_theta = Poly(theta_minpoly, t, domain='QQ')
        h1 = p_theta.is_irreducible
        
        valid_autos = True
        autos_set = set()
        for sigma in automorphisms:
            rem = Poly(p_theta.subs(t, sigma), t, domain='QQ') % p_theta
            if not rem.is_zero:
                valid_autos = False
                break
            rem_sigma = Poly(sigma, t, domain='QQ') % p_theta
            autos_set.add(rem_sigma.as_expr())
            
        if len(autos_set) != p_theta.degree():
            valid_autos = False
            
        h1 = bool(h1 and valid_autos)
    except Exception:
        h1 = False
        
    # H2: alpha is an element of L
    try:
        Poly(alpha_expr, t, domain='QQ')
        h2 = True
    except Exception:
        h2 = False
        
    # Conclusion: The minimal polynomial of alpha over K is exactly prod_{beta in O(alpha)} (x - beta)
    try:
        p_theta = Poly(theta_minpoly, t, domain='QQ')
        orbit_polys = set()
        for sigma in autos_set:
            beta = Poly(alpha_expr.subs(t, sigma), t, domain='QQ') % p_theta
            orbit_polys.add(beta.as_expr())
            
        prod_expr = sp.Integer(1)
        for beta_expr in orbit_polys:
            prod_expr = prod_expr * (x - beta_expr)
            
        prod_expr = sp.expand(prod_expr)
        prod_poly = Poly(prod_expr, x)
        
        reduced_coeffs = []
        is_in_K = True
        for c in prod_poly.all_coeffs():
            c_poly = Poly(c, t, domain='QQ') % p_theta
            if c_poly.degree() > 0:
                is_in_K = False
                break
            reduced_coeffs.append(c_poly.nth(0))
            
        if not is_in_K:
            neg_q = True
        else:
            prod_in_x = Poly(reduced_coeffs, x, domain='QQ')
            # The product is the minimal polynomial iff it is irreducible over K
            if prod_in_x.is_irreducible:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension of fields with Galois group G",
    "H_2: alpha is an element of L",
    "not Q: The minimal polynomial of alpha over K is NOT exactly prod_{beta in O(alpha)} (x - beta)"
]

N_HYP = 2
NEG_Q_INDEX = 2