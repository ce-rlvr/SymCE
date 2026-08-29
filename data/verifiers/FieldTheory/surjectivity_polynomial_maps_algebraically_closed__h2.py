import sympy
from sympy import *
from sympy.abc import *
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        K, f = witness
    else:
        K = S.Complexes
        f = witness

    if callable(f):
        try:
            x_sym = Symbol('x')
            f = f(x_sym)
        except Exception:
            pass

    if isinstance(f, str):
        try:
            f = sympify(f)
        except Exception:
            pass

    # H_1: K is an algebraically closed field
    try:
        h1 = False
        if K == S.Complexes:
            h1 = True
        elif hasattr(K, 'is_algebraically_closed') and K.is_algebraically_closed:
            h1 = True
        elif str(K) in ['CC', 'Complexes', 'Complex Field']:
            h1 = True
    except Exception:
        h1 = False

    # H_2: f is non-constant
    try:
        h2 = False
        if isinstance(f, Expr):
            f_simp = simplify(f)
            if len(f_simp.free_symbols) > 0:
                h2 = True
        elif isinstance(f, (list, tuple, Matrix)):
            for comp in f:
                if isinstance(comp, Expr) and len(simplify(comp).free_symbols) > 0:
                    h2 = True
                    break
        elif hasattr(f, 'is_constant'):
            h2 = not f.is_constant()
    except Exception:
        h2 = False

    # neg_Q: The polynomial map c -> f(c) is NOT surjective from K onto K
    try:
        neg_q = False
        if isinstance(f, Expr):
            f_simp = simplify(f)
            vars_list = list(f_simp.free_symbols)
            if len(vars_list) == 0:
                neg_q = True
            elif len(vars_list) == 1:
                x_var = vars_list[0]
                num, den = f_simp.as_numer_denom()
                if den != 1 or not f_simp.is_polynomial(x_var):
                    neg_q = True
                else:
                    deg = degree(f_simp, x_var)
                    if K == S.Complexes or str(K) in ['CC', 'Complexes', 'Complex Field'] or (hasattr(K, 'is_algebraically_closed') and K.is_algebraically_closed):
                        neg_q = False
                    elif K == S.Reals or str(K) in ['RR', 'Reals', 'Real Field']:
                        if deg % 2 == 0:
                            neg_q = True
                        else:
                            neg_q = False
                    elif K == S.Rationals or str(K) in ['QQ', 'Rationals', 'Rational Field']:
                        if deg > 1:
                            neg_q = True
                        else:
                            neg_q = False
                    else:
                        if deg == 1:
                            neg_q = False
                        else:
                            neg_q = True
            else:
                num, den = f_simp.as_numer_denom()
                if den != 1:
                    neg_q = True
                else:
                    if K == S.Complexes or str(K) in ['CC', 'Complexes', 'Complex Field'] or (hasattr(K, 'is_algebraically_closed') and K.is_algebraically_closed):
                        neg_q = False
                    else:
                        neg_q = True
        elif isinstance(f, (list, tuple, Matrix)):
            m = len(f) if isinstance(f, (list, tuple)) else f.shape[0]
            all_vars = set()
            for comp in f:
                if isinstance(comp, Expr):
                    all_vars.update(simplify(comp).free_symbols)
            n = len(all_vars)
            if m > n:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f is non-constant",
    "¬Q: The polynomial map c -> f(c) is not surjective from K onto K"
]

N_HYP = 2
NEG_Q_INDEX = 2