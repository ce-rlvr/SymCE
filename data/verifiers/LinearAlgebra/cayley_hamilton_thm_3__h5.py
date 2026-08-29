import sympy
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, t
import itertools

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

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n x n matrix with entries in F",
    "H_3: p(t) is the characteristic polynomial of A",
    "H_4: m(t) is the minimal polynomial of A",
    "¬Q: The set of roots of p(t) is not equal to the set of roots of m(t)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def eval_poly_matrix(poly_expr, var, A):
    p = sympy.Poly(poly_expr, var)
    coeffs = p.all_coeffs()
    n = A.shape[0]
    res = sympy.zeros(n, n)
    degree = len(coeffs) - 1
    for i in range(degree, -1, -1):
        res += coeffs[degree - i] * (A ** i)
    return res

def conditions(witness):
    A = None
    p_expr = None
    m_expr = None
    
    if isinstance(witness, tuple):
        if len(witness) == 3:
            A, p_expr, m_expr = witness
        elif len(witness) == 4:
            _, A, p_expr, m_expr = witness
        elif len(witness) == 2:
            A, p_expr = witness
        elif len(witness) >= 1:
            A = witness[0]
    else:
        A = witness

    # H1: F is a field
    try:
        h1 = isinstance(A, sympy.MatrixBase)
    except Exception:
        h1 = False

    # H2: A is an n x n matrix
    try:
        h2 = A.is_square
    except Exception:
        h2 = False

    var = sympy.Symbol('t')
    try:
        if p_expr is not None:
            free = getattr(p_expr, "free_symbols", set()) - getattr(A, "free_symbols", set())
            if free:
                var = sorted(list(free), key=lambda s: s.name)[0]
        elif m_expr is not None:
            free = getattr(m_expr, "free_symbols", set()) - getattr(A, "free_symbols", set())
            if free:
                var = sorted(list(free), key=lambda s: s.name)[0]
    except Exception:
        pass

    # H3: p(t) is the characteristic polynomial of A
    try:
        if p_expr is None:
            p_expr = A.charpoly(var).as_expr()
            h3 = True
        else:
            if hasattr(p_expr, 'as_expr'):
                p_expr = p_expr.as_expr()
            cp = A.charpoly(var).as_expr()
            h3 = bool(sympy.simplify(p_expr - cp) == 0)
    except Exception:
        h3 = False

    # H4: m(t) is the minimal polynomial of A
    try:
        if m_expr is None:
            cp = A.charpoly(var).as_expr()
            factors = sympy.factor_list(cp)[1]
            ranges = [range(1, mult + 1) for _, mult in factors]
            found = False
            for exps in itertools.product(*ranges):
                test_poly = sympy.Integer(1)
                for (f, _), e in zip(factors, exps):
                    test_poly = test_poly * (f ** e)
                test_poly = sympy.expand(test_poly)
                if eval_poly_matrix(test_poly, var, A).is_zero_matrix:
                    m_expr = test_poly
                    found = True
                    break
            h4 = found
        else:
            if hasattr(m_expr, 'as_expr'):
                m_expr = m_expr.as_expr()
            
            p_m = sympy.Poly(m_expr, var)
            if p_m.LC() != 1:
                h4 = False
            elif not eval_poly_matrix(m_expr, var, A).is_zero_matrix:
                h4 = False
            else:
                factors = sympy.factor_list(m_expr)[1]
                h4 = True
                for f, _ in factors:
                    q = sympy.simplify(m_expr / f)
                    if eval_poly_matrix(q, var, A).is_zero_matrix:
                        h4 = False
                        break
    except Exception:
        h4 = False

    # ¬Q: lambda is a root of p(t) iff lambda is a root of m(t) FAILS
    try:
        if p_expr is not None and m_expr is not None:
            sp = sympy.sqf_part(p_expr, var)
            sm = sympy.sqf_part(m_expr, var)
            poly_p = sympy.Poly(sp, var)
            poly_m = sympy.Poly(sm, var)
            same_roots = (poly_p.monic() == poly_m.monic())
            neg_q = not same_roots
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]