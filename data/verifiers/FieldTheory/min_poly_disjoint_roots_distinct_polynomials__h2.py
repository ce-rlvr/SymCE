import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x
from sympy.polys import minimal_polynomial
import itertools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_minpoly(alpha, x_var, domain=None):
    """Helper to compute the minimal polynomial of an element or matrix."""
    if hasattr(alpha, 'charpoly'):
        cp = alpha.charpoly(x_var).as_expr()
        if domain is not None:
            try:
                factors = sympy.factor_list(cp, domain=domain)[1]
            except Exception:
                factors = sympy.factor_list(cp)[1]
        else:
            factors = sympy.factor_list(cp)[1]
            
        ranges = [range(1, mult + 1) for factor, mult in factors]
        best_poly = cp
        best_deg = sympy.degree(cp, x_var)
        
        for mults in itertools.product(*ranges):
            poly = sympy.prod([factor**m for (factor, _), m in zip(factors, mults)])
            poly = sympy.expand(poly)
            coeffs = sympy.Poly(poly, x_var).all_coeffs()
            
            val = sympy.zeros(alpha.rows, alpha.cols)
            M_pow = sympy.eye(alpha.rows)
            for c in reversed(coeffs):
                val += c * M_pow
                M_pow = M_pow * alpha
            
            if domain is not None and hasattr(domain, 'characteristic') and domain.characteristic > 0:
                val = val.applyfunc(lambda v: v % domain.characteristic)
                
            if val.is_zero_matrix:
                deg = sympy.degree(poly, x_var)
                if deg < best_deg:
                    best_poly = poly
                    best_deg = deg
                    
        if domain is not None:
            try:
                return sympy.Poly(best_poly, x_var, domain=domain).monic().as_expr()
            except Exception:
                return sympy.Poly(best_poly, x_var).monic().as_expr()
        else:
            return sympy.Poly(best_poly, x_var).monic().as_expr()
    else:
        return minimal_polynomial(alpha, x_var, domain=domain)

def conditions(witness) -> list[bool]:
    F = None
    alpha = None
    beta = None
    f = None
    g = None
    
    # Parse witness
    if isinstance(witness, dict):
        F = witness.get('F')
        alpha = witness.get('alpha')
        beta = witness.get('beta')
        f = witness.get('f')
        g = witness.get('g')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            F, a, b = witness
            if isinstance(a, sympy.Poly):
                f, g = a.as_expr(), b.as_expr()
            elif isinstance(a, sympy.Expr) and len(a.free_symbols) == 1 and not a.is_number:
                f, g = a, b
                sym = list(a.free_symbols)[0]
                if sym != x:
                    f = f.subs(sym, x)
                    g = g.subs(sym, x)
            else:
                alpha, beta = a, b
        elif len(witness) == 5:
            F, alpha, beta, f, g = witness

    # Map common sets to domains
    if F == sympy.S.Rationals:
        F = sympy.QQ
    elif F == sympy.S.Reals:
        F = sympy.RR
    elif F == sympy.S.Complexes:
        F = sympy.CC
    elif F == sympy.S.Integers:
        F = sympy.ZZ

    # Convert lists to matrices if applicable
    if isinstance(alpha, list) and len(alpha) > 0 and isinstance(alpha[0], list):
        alpha = sympy.Matrix(alpha)
    if isinstance(beta, list) and len(beta) > 0 and isinstance(beta[0], list):
        beta = sympy.Matrix(beta)

    if isinstance(f, sympy.Poly):
        f = f.as_expr()
    if isinstance(g, sympy.Poly):
        g = g.as_expr()

    # H_1: F is a field
    try:
        if hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        else:
            h1 = F in [sympy.QQ, sympy.RR, sympy.CC]
    except Exception:
        h1 = False

    # Compute minimal polynomials if not provided
    if f is None and alpha is not None:
        try:
            f = get_minpoly(alpha, x, domain=F)
        except Exception:
            pass
    if g is None and beta is not None:
        try:
            g = get_minpoly(beta, x, domain=F)
        except Exception:
            pass

    # Normalize f and g to be monic
    try:
        if f is not None:
            f = sympy.Poly(f, x, domain=F).monic().as_expr()
        if g is not None:
            g = sympy.Poly(g, x, domain=F).monic().as_expr()
    except Exception:
        pass

    # H_2: The minimal polynomial of α over F is distinct from the minimal polynomial of β over F
    try:
        h2 = False
        if f is not None and g is not None:
            h2 = bool(sympy.simplify(f - g) != 0)
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of α over F and the minimal polynomial of β over F HAVE a common root in some extension field
    # This is equivalent to their GCD over F having degree > 0
    try:
        neg_q = False
        if f is not None and g is not None:
            poly_f = sympy.Poly(f, x, domain=F)
            poly_g = sympy.Poly(g, x, domain=F)
            gcd_fg = poly_f.gcd(poly_g)
            neg_q = gcd_fg.degree() > 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The minimal polynomial of α over F is distinct from the minimal polynomial of β over F",
    "¬Q: The minimal polynomial of α over F and the minimal polynomial of β over F have a common root in some extension field of F"
]

N_HYP = 2
NEG_Q_INDEX = 2