import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Poly, factor_list, simplify, Symbol, QQ, ZZ, I, sqrt
from sympy.abc import x, y, z

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
    r"H_1: K is a field",
    r"H_2: f(x) is irreducible over K",
    r"H_3: There exists a root \alpha of f(x) in its splitting field such that g(x) - \alpha is irreducible over K(\alpha)",
    r"¬Q: The composed polynomial f(g(x)) is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false Capelli's Lemma conjecture.
    The witness should be a dictionary with keys:
      'K': SymPy domain (e.g., QQ)
      'x': SymPy symbol used as the variable
      'f': SymPy expression for f(x)
      'g': SymPy expression for g(x)
      'alpha': SymPy expression for the root \alpha
    """
    try:
        K = witness.get('K')
        x_var = witness.get('x', x)
        f = witness.get('f')
        g = witness.get('g')
        alpha = witness.get('alpha')
    except Exception:
        return [False, False, False, False]
        
    # H_1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    # H_2: f(x) is irreducible over K
    try:
        poly_f = Poly(f, x_var, domain=K)
        if poly_f.degree() <= 0:
            h2 = False
        else:
            _, factors = factor_list(f, x_var, domain=K)
            non_const = sum(mult for fac, mult in factors if Poly(fac, x_var).degree() > 0)
            h2 = (non_const == 1)
    except Exception:
        h2 = False
        
    # H_3: alpha is a root of f, and g(x) - alpha is irreducible over K(alpha)
    try:
        val = simplify(f.subs(x_var, alpha))
        is_root = (val == 0)
        
        if not is_root:
            h3 = False
        else:
            expr = g - alpha
            p = Poly(expr, x_var)
            # Any degree 1 polynomial is irreducible over any field
            if p.degree() == 1:
                h3 = True
            else:
                _, factors = factor_list(expr, x_var, extension=alpha)
                non_const = sum(mult for fac, mult in factors if Poly(fac, x_var).degree() > 0)
                h3 = (non_const == 1)
    except Exception:
        h3 = False
        
    # ¬Q: f(g(x)) is NOT irreducible over K
    try:
        fg = f.subs(x_var, g)
        try:
            poly_fg = Poly(fg, x_var, domain=K)
            is_in_K = True
        except Exception:
            is_in_K = False
            
        if not is_in_K:
            # If f(g(x)) is not in K[x], it cannot be irreducible over K
            neg_q = True
        else:
            if poly_fg.degree() <= 0:
                neg_q = True
            else:
                _, factors = factor_list(fg, x_var, domain=K)
                non_const = sum(mult for fac, mult in factors if Poly(fac, x_var).degree() > 0)
                neg_q = (non_const != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]