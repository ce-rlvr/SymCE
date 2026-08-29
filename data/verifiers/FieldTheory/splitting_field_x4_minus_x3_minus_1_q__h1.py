import sympy
from sympy import Symbol, Poly, discriminant, sqrt
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

x = Symbol('x')

def conditions(witness):
    h1_ok = False
    poly_witness = witness
    
    # If the witness is provided as a tuple (e.g., (polynomial, group)), extract the polynomial
    if isinstance(witness, tuple) and len(witness) > 0:
        poly_witness = witness[0]
        
    try:
        syms = poly_witness.free_symbols
        if len(syms) == 1:
            var = list(syms)[0]
        elif len(syms) == 0:
            var = Symbol('x')
        else:
            var = None
            
        if var is not None:
            p = Poly(poly_witness, var)
            if p.domain.is_QQ or p.domain.is_ZZ:
                h1_ok = True
    except Exception:
        pass

    neg_q = False
    try:
        if h1_ok:
            q_true = False
            factors = p.factor_list()[1]
            s4_quartic_found = False
            q_true_possible = True
            
            quartic_discriminant = None
            
            # First pass: look for an irreducible quartic with Galois group S4
            for fac, mult in factors:
                if fac.degree() == 4:
                    d = discriminant(fac.as_expr(), var)
                    if sqrt(d).is_rational:
                        continue  # Galois group is a subgroup of A4, not S4
                    
                    fac_monic = fac.monic()
                    coeffs = fac_monic.all_coeffs()
                    a, b, c, d_coeff = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
                    y = Symbol('y')
                    # Resolvent cubic: y^3 - b*y^2 + (a*c - 4*d)*y - a^2*d + 4*b*d - c^2
                    resolvent = y**3 - b*y**2 + (a*c - 4*d_coeff)*y - a**2*d_coeff + 4*b*d_coeff - c**2
                    res_p = Poly(resolvent, y)
                    
                    if res_p.is_irreducible:
                        if s4_quartic_found:
                            # Multiple S4 quartics might generate a larger compositum
                            q_true_possible = False
                        s4_quartic_found = True
                        quartic_discriminant = d
            
            # Second pass: ensure all other factors have splitting fields contained within the S4 extension
            if s4_quartic_found and q_true_possible:
                for fac, mult in factors:
                    if fac.degree() == 1:
                        continue
                    elif fac.degree() == 4:
                        d = discriminant(fac.as_expr(), var)
                        if d != quartic_discriminant:
                            q_true_possible = False
                            break
                    elif fac.degree() in (2, 3):
                        d_fac = discriminant(fac.as_expr(), var)
                        if d_fac == 0:
                            q_true_possible = False
                            break
                        # The subfield is contained iff the discriminants differ by a rational square
                        ratio = quartic_discriminant / d_fac
                        if not sqrt(ratio).is_rational:
                            q_true_possible = False
                            break
                    else:
                        # Degrees > 4 cannot be contained in an S4 extension without changing the group
                        q_true_possible = False
                        break
                        
            if q_true_possible and s4_quartic_found:
                q_true = True
                
            neg_q = not q_true
        else:
            # If it's not a valid polynomial over Q, the conclusion fails
            neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The degree of the splitting field is not 24 or the Galois group is not S4"
]

N_HYP = 1
NEG_Q_INDEX = 1