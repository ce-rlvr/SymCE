import sympy
from sympy import Poly, sqrt
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_galois_group_S4(f):
    """
    Checks if the Galois group of the splitting field of f(x) over QQ is S4.
    This uses the standard resolvent cubic and discriminant method for degree 4 polynomials.
    """
    try:
        syms = list(f.free_symbols)
        if len(syms) != 1:
            return False
        var = syms[0]
        f_poly = Poly(f, var, domain='QQ')
        
        # Factor the polynomial over QQ
        _, irreps = f_poly.factor_list()
        # Consider only non-linear irreducible factors
        irreps = [p for p, m in irreps if p.degree() > 1]
        
        if not irreps:
            return False
            
        # If there is exactly one non-linear irreducible factor and its degree is 4
        if len(irreps) == 1 and irreps[0].degree() == 4:
            p = irreps[0].monic()
            coeffs = p.all_coeffs()
            # coeffs for monic degree 4: [1, a, b, c, d]
            a, b, c, d = coeffs[1], coeffs[2], coeffs[3], coeffs[4]
            
            # Construct the resolvent cubic
            R = Poly(var**3 - b*var**2 + (a*c - 4*d)*var - a**2*d + 4*b*d - c**2, var, domain='QQ')
            
            # For an irreducible quartic, the Galois group is S4 iff the resolvent cubic 
            # is irreducible and the discriminant is not a perfect square in QQ.
            if R.is_irreducible:
                Delta = p.discriminant()
                if not sqrt(Delta).is_rational:
                    return True
            return False
            
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    Returns a list of booleans: [H_1_ok, neg_Q_ok]
    """
    # H_1: Let E be the splitting field of f(x) over QQ
    # This implies the witness must be a valid non-constant polynomial over QQ.
    try:
        syms = list(witness.free_symbols)
        if len(syms) != 1:
            h1_ok = False
        else:
            var = syms[0]
            f_poly = Poly(witness, var, domain='QQ')
            h1_ok = f_poly.degree() >= 1
    except Exception:
        h1_ok = False

    # neg_Q: The Galois group Gal(E/QQ) is NOT isomorphic to S4
    try:
        if not h1_ok:
            neg_q = False
        else:
            neg_q = not is_galois_group_S4(witness)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial over QQ",
    "¬Q: The Galois group of f(x) over QQ is not isomorphic to S4"
]

N_HYP = 1
NEG_Q_INDEX = 1