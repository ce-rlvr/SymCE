import sympy
from sympy import Symbol, expand, simplify, Eq, Poly
from sympy import minpoly

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F', None)
        alpha = witness.get('alpha')
        t = witness.get('t')
        p = witness.get('p')
        x = witness.get('x')
    elif isinstance(witness, tuple):
        if len(witness) == 5:
            F, alpha, t, p, x = witness
        elif len(witness) == 4:
            alpha, t, p, x = witness
            F = None
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        if F is None:
            h1 = True
        else:
            h1 = getattr(F, 'is_Field', False) or F in [sympy.S.Reals, sympy.S.Complexes, sympy.QQ]
    except Exception:
        h1 = False

    # H_2: alpha is an algebraic element over F
    try:
        mp = minpoly(alpha, x)
        h2 = True
    except Exception:
        h2 = False

    # H_3: t is a transcendental element over F
    try:
        if hasattr(t, 'is_Symbol') and t.is_Symbol:
            h3 = True
        elif hasattr(t, 'is_transcendental') and t.is_transcendental:
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: p(x) is not the minimal polynomial of alpha over F(t)
    try:
        if isinstance(p, Eq):
            p_expr = p.lhs - p.rhs
        else:
            p_expr = p
        if hasattr(p_expr, 'as_expr'):
            p_expr = p_expr.as_expr()
            
        p_val = simplify(p_expr.subs(x, alpha))
        if p_val != 0:
            neg_q = True
        else:
            try:
                poly_p = Poly(p_expr, x)
                lc = poly_p.LC()
            except Exception:
                lc = None
                
            if lc != 1:
                neg_q = True
            else:
                if F is None or F == sympy.QQ:
                    expected_p = minpoly(alpha, x)
                    if simplify(expand(p_expr - expected_p)) == 0:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    if poly_p.degree() == 1:
                        neg_q = False
                    else:
                        expected_p = minpoly(alpha, x)
                        if simplify(expand(p_expr - expected_p)) == 0:
                            neg_q = False
                        else:
                            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: t is a transcendental element over F",
    "¬Q: p(x) is not the minimal polynomial of alpha over F(t)"
]

N_HYP = 3
NEG_Q_INDEX = 3