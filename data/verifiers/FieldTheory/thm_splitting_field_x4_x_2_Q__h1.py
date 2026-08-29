import sympy as sp
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    # H_1: Let K be the splitting field of f(x) over Q
    # This implies the witness must be a valid polynomial in x with rational coefficients.
    try:
        if isinstance(witness, sp.Poly):
            if witness.gen != x:
                h1 = False
            else:
                h1 = all(c.is_Rational for c in witness.coeffs())
        elif isinstance(witness, sp.Expr):
            if not witness.free_symbols.issubset({x}):
                h1 = False
            else:
                p = sp.Poly(witness, x)
                h1 = all(c.is_Rational for c in p.coeffs())
        elif isinstance(witness, (int, float, sp.Rational, sp.Integer, sp.Float)):
            p = sp.Poly(witness, x)
            h1 = all(c.is_Rational for c in p.coeffs())
        else:
            h1 = False
    except Exception:
        h1 = False

    # Conclusion: The degree of the extension [K : Q] is 24, and the Galois group of K over Q is isomorphic to S4.
    # We check if the splitting field of the witness has degree 24 and Galois group S4.
    try:
        if isinstance(witness, sp.Poly):
            expr = witness.as_expr()
        else:
            expr = witness
            
        p = sp.Poly(expr, x, domain='QQ')
        
        # If the degree is less than 4, the splitting field degree divides d! < 24.
        if p.degree() < 4:
            has_S4 = False
        else:
            factors = p.factor_list()[1]
            deg4_factors = [fac for fac, mult in factors if fac.degree() == 4]
            
            if not deg4_factors:
                has_S4 = False
            elif len(deg4_factors) == 1:
                p4 = deg4_factors[0]
                disc = sp.discriminant(p4.as_expr(), x)
                
                # For an irreducible quartic, Galois group is a subgroup of A4 iff discriminant is a perfect square.
                if sp.sqrt(disc).is_rational:
                    has_S4 = False
                else:
                    coeffs = p4.all_coeffs()
                    lead = coeffs[0]
                    a = coeffs[1]/lead
                    b = coeffs[2]/lead
                    c = coeffs[3]/lead
                    d = coeffs[4]/lead
                    
                    # Resolvent cubic of x^4 + ax^3 + bx^2 + cx + d
                    res_cubic = x**3 - b*x**2 + (a*c - 4*d)*x - a**2*d + 4*b*d - c**2
                    res_p = sp.Poly(res_cubic, x, domain='QQ')
                    
                    # If the resolvent cubic is reducible, the Galois group is D4 or V4.
                    if not res_p.is_irreducible:
                        has_S4 = False
                    else:
                        has_S4 = True
                        # Ensure any other factors have their splitting fields contained in the S4 extension
                        for fac, mult in factors:
                            if fac.degree() == 1:
                                continue
                            if fac.degree() == 2:
                                fac_disc = sp.discriminant(fac.as_expr(), x)
                                if not sp.sqrt(disc * fac_disc).is_rational:
                                    has_S4 = False
                                    break
                            elif fac.degree() > 2 and fac != p4:
                                q, rem = res_p.div(fac)
                                if not rem.is_zero:
                                    has_S4 = False
                                    break
            else:
                # Multiple degree 4 factors or higher degree factors
                has_S4 = False
    except Exception:
        has_S4 = False

    neg_q = not has_S4

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The splitting field of f(x) does not have degree 24 or its Galois group is not S4"
]

N_HYP = 1
NEG_Q_INDEX = 1