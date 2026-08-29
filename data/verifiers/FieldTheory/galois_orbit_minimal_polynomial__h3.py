import sympy as sp
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

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: alpha is an element of E",
    "¬Q: The minimal polynomial of alpha over F is NOT given by the product over the Galois orbit"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    The witness is expected to be a tuple: (P_expr, autos, alpha_expr)
    where:
      - P_expr is the minimal polynomial of a primitive element of E over Q (defining E/Q).
      - autos is a list of polynomials representing the automorphisms in Gal(E/Q).
      - alpha_expr is a polynomial representing alpha in E.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 3:
            return [False, False, False]
            
        P_expr = sp.sympify(witness[0])
        autos = [sp.sympify(a) for a in witness[1]]
        alpha_expr = sp.sympify(witness[2])
        
        syms = P_expr.free_symbols
        if len(syms) == 1:
            x = list(syms)[0]
        elif len(syms) == 0:
            x = sp.Symbol('x')
        else:
            return [False, False, False]
            
        y = sp.Symbol('y')
        if y == x:
            y = sp.Symbol('z')
            
        P = sp.Poly(P_expr, x, domain='QQ')
    except Exception:
        return [False, False, False]
        
    # H_1: E/F is a finite Galois extension
    h1_ok = False
    try:
        if P.degree() > 0 and P.is_irreducible:
            if len(autos) == P.degree():
                valid_autos = True
                seen = set()
                for A_expr in autos:
                    A_poly = sp.Poly(A_expr, x, domain='QQ')
                    P_A = sp.Poly(P_expr.subs(x, A_expr), x, domain='QQ')
                    rem = P_A.rem(P)
                    if not rem.is_zero:
                        valid_autos = False
                        break
                    
                    A_mod = A_poly.rem(P).as_expr()
                    A_mod_simp = sp.expand(A_mod)
                    if A_mod_simp in seen:
                        valid_autos = False
                        break
                    seen.add(A_mod_simp)
                if valid_autos:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: alpha is an element of E
    h2_ok = False
    try:
        alpha_poly = sp.Poly(alpha_expr, x, domain='QQ')
        h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The minimal polynomial of alpha over F is NOT given by the product over the Galois orbit
    # The false conjecture assumes the product over the multiset of images (i.e., the characteristic polynomial)
    # is always the minimal polynomial. This fails when alpha is not a primitive element.
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            roots_in_E = []
            for A_expr in autos:
                alpha_A = sp.Poly(alpha_expr.subs(x, A_expr), x, domain='QQ').rem(P).as_expr()
                roots_in_E.append(alpha_A)
            
            prod_expr = 1
            for r in roots_in_E:
                prod_expr = prod_expr * (y - r)
            
            prod_expr = sp.expand(prod_expr)
            prod_poly_y = sp.Poly(prod_expr, y)
            
            reduced_coeffs = []
            for c in prod_poly_y.all_coeffs():
                c_poly = sp.Poly(c, x, domain='QQ')
                c_reduced = c_poly.rem(P).as_expr()
                reduced_coeffs.append(c_reduced)
            
            is_in_F = True
            char_poly_coeffs = []
            for c in reduced_coeffs:
                c_poly = sp.Poly(c, x)
                if not c_poly.is_constant():
                    is_in_F = False
                    break
                char_poly_coeffs.append(sp.Rational(c.subs(x, 0)))
            
            if is_in_F:
                char_poly = sp.Poly(char_poly_coeffs, y, domain='QQ')
                # The minimal polynomial is the square-free part of the characteristic polynomial
                min_poly = sp.sqf_part(char_poly)
                
                char_poly = char_poly.monic()
                min_poly = min_poly.monic()
                
                if char_poly != min_poly:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]