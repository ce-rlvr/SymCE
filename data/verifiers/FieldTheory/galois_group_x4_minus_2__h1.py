import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x
from sympy import Poly, Rational, Dummy, sqrt

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_irreducible_quartic_D8(p):
    """
    Checks if an irreducible monic quartic polynomial over QQ has Galois group D8.
    """
    try:
        coeffs = p.all_coeffs()
        a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
        
        y = Dummy('y')
        # Depress the quartic: substitute x = y - a/4
        p_depressed = p.expr.subs(x, y - a/Rational(4)).expand()
        p_dep = Poly(p_depressed, y, domain='QQ')
        
        dep_coeffs = p_dep.all_coeffs()
        if len(dep_coeffs) != 5:
            return True
            
        p_c = dep_coeffs[2]
        q_c = dep_coeffs[3]
        r_c = dep_coeffs[4]
        
        # Resolvent cubic for depressed quartic
        z = Dummy('z')
        R = Poly(z**3 - p_c*z**2 - 4*r_c*z + 4*p_c*r_c - q_c**2, z, domain='QQ')
        
        R_factors = R.factor_list()[1]
        rational_roots = []
        for factor, mult in R_factors:
            if factor.degree() == 1:
                A = factor.all_coeffs()[0]
                B = factor.all_coeffs()[1]
                rational_roots.append(-B / A)
                
        # D8 and C4 have exactly 1 rational root in the resolvent cubic
        if len(rational_roots) != 1:
            return False
            
        z0 = rational_roots[0]
        
        # Distinguish C4 and D8
        val = z0**2 - 4*r_c
        if val == 0:
            return False
            
        if sqrt(val).is_Rational:
            return False
            
        Delta = p.discriminant()
        
        if sqrt(val * Delta).is_Rational:
            return False
            
        return True
    except Exception:
        # Safe fallback: assume it might be D8 to avoid falsely accepting an invalid counterexample
        return True

def conditions(witness):
    # H_1: E is the splitting field of f(x) over Q
    # This hypothesis simply requires the witness to be a valid polynomial over Q.
    try:
        p = Poly(witness, x, domain='QQ')
        h1_ok = True
    except Exception:
        h1_ok = False
        
    # neg_Q: The Galois group Gal(E/Q) is NOT isomorphic to D8
    try:
        if not h1_ok:
            neg_q = False
        else:
            if p.degree() == 0:
                is_d8 = False
            else:
                p_sqf = p.sqf_part()
                factors = p_sqf.factor_list()[1]
                non_linear = [f for f, mult in factors if f.degree() > 1]
                
                if not non_linear:
                    is_d8 = False
                else:
                    degrees = [f.degree() for f in non_linear]
                    
                    possible = True
                    for d in degrees:
                        if 8 % d != 0:
                            possible = False
                            break
                            
                    if not possible:
                        is_d8 = False
                    elif max(degrees) <= 2:
                        # Compositum of abelian extensions is abelian, D8 is non-abelian
                        is_d8 = False
                    elif max(degrees) == 8:
                        # Safe fallback for degree 8 factors
                        is_d8 = True
                    else:
                        # Max degree is 4. Check if any degree 4 factor has Galois group D8.
                        has_D8_quartic = False
                        for f in non_linear:
                            if f.degree() == 4:
                                lc = f.LC()
                                f_monic = f.quo(Poly(lc, x, domain='QQ'))
                                if is_irreducible_quartic_D8(f_monic):
                                    has_D8_quartic = True
                                    break
                        is_d8 = has_D8_quartic
                        
            neg_q = not is_d8
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: E is the splitting field of f(x) over Q",
    "¬Q: The Galois group Gal(E/Q) is not isomorphic to the dihedral group D8"
]

N_HYP = 1
NEG_Q_INDEX = 1