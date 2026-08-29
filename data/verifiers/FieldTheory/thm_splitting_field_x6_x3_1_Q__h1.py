import sympy
from sympy import Poly, cyclotomic_poly, divisors
from sympy.abc import x

# Setup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "¬Q: The splitting field of f(x) over Q does not have degree 6 or its Galois group is not C6"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    import sympy
    from sympy import Poly, cyclotomic_poly, divisors
    from sympy.abc import x
    
    # H_1: witness is a polynomial over Q
    try:
        witness_expr = sympy.sympify(witness)
        free_syms = witness_expr.free_symbols
        if len(free_syms) == 0:
            var = x
            p = Poly(witness_expr, var)
        elif len(free_syms) == 1:
            var = list(free_syms)[0]
            p = Poly(witness_expr, var)
        else:
            h1 = False
            p = None
            
        if p is not None:
            h1 = all(c.is_rational for c in p.coeffs())
    except Exception:
        h1 = False
        p = None
        
    # neg_Q: splitting field degree is not 6 OR Galois group is not C6
    try:
        if not h1 or p is None:
            neg_q = False
        else:
            factors = p.factor_list()[1]
            irreducibles = [fac[0].as_expr() for fac in factors]
            
            is_c6_ext = False
            # Check if the splitting field is one of the known C6 cyclotomic fields
            # The original theorem is about Phi_9(x) = x^6 + x^3 + 1
            for n in [7, 9, 14, 18]:
                phi_n = cyclotomic_poly(n, var)
                has_phi_n = False
                for fac_expr in irreducibles:
                    fac_poly = Poly(fac_expr, var)
                    if fac_poly.degree() == 6:
                        c = fac_poly.LC()
                        if (fac_expr / c).expand() == phi_n.expand():
                            has_phi_n = True
                            break
                if has_phi_n:
                    allowed_phis = [cyclotomic_poly(d, var).expand() for d in divisors(n)]
                    all_allowed = True
                    for fac_expr in irreducibles:
                        fac_poly = Poly(fac_expr, var)
                        c = fac_poly.LC()
                        fac_monic = (fac_expr / c).expand()
                        if fac_monic not in allowed_phis:
                            all_allowed = False
                            break
                    if all_allowed:
                        is_c6_ext = True
                        break
            
            if is_c6_ext:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]