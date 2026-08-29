import sympy
from sympy import Symbol, Poly, sympify, QQ, roots
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = ["H_1: f is a polynomial over F", "H_2: K is a splitting field of f over F", "H_3: E is an intermediate field between F and K", "neg_Q: K is not a splitting field of f over E"]

N_HYP = 3
NEG_Q_INDEX = 3

def get_domain(gens):
    filtered_gens = [g for g in gens if not sympify(g).is_Rational]
    if not filtered_gens:
        return QQ
    return QQ.algebraic_field(*filtered_gens)

def is_in_field(expr, gens):
    expr = sympify(expr)
    if expr.is_Rational:
        return True
    try:
        dom = get_domain(gens)
        dom.from_sympy(expr)
        return True
    except Exception:
        try:
            from sympy import minpoly
            y = Symbol('y')
            dom = get_domain(gens)
            mp = minpoly(expr, y, domain=dom)
            return mp.degree() == 1
        except Exception:
            return False

def conditions(witness):
    x = Symbol('x')
    try:
        if isinstance(witness, dict):
            F_gens = witness.get('F', [])
            E_gens = witness.get('E', [])
            K_gens = witness.get('K', [])
            f = witness.get('f', x)
        else:
            F_gens, E_gens, K_gens, f = witness
            
        if hasattr(f, 'as_expr'):
            f_expr = f.as_expr()
            if hasattr(f, 'gens') and f.gens:
                x_sym = f.gens[0]
            else:
                x_sym = x
        else:
            f_expr = sympify(f)
            free = f_expr.free_symbols
            x_sym = list(free)[0] if free else x

        F_gens = [sympify(g) for g in F_gens]
        E_gens = [sympify(g) for g in E_gens]
        K_gens = [sympify(g) for g in K_gens]

    except Exception:
        return [False, False, False, False]

    # H1: f is a polynomial over F
    try:
        f_poly = Poly(f_expr, x_sym)
        h1 = True
        for coeff in f_poly.coeffs():
            if not is_in_field(coeff, F_gens):
                h1 = False
                break
    except Exception:
        h1 = False
        f_poly = None

    # H2: K is a splitting field of f over F
    try:
        if f_poly is None:
            h2 = False
        else:
            rts = roots(f_expr, x_sym)
            if sum(rts.values()) != f_poly.degree():
                h2 = False
            else:
                h2 = True
                for r in rts:
                    if not is_in_field(r, K_gens):
                        h2 = False
                        break
                if h2:
                    F_and_roots = list(F_gens) + list(rts.keys())
                    for g in K_gens:
                        if not is_in_field(g, F_and_roots):
                            h2 = False
                            break
    except Exception:
        h2 = False

    # H3: E is an intermediate field between F and K
    try:
        h3 = True
        for g in F_gens:
            if not is_in_field(g, E_gens):
                h3 = False
                break
        if h3:
            for g in E_gens:
                if not is_in_field(g, K_gens):
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: K is NOT a splitting field of f over E
    try:
        if f_poly is None:
            neg_q = False
        else:
            rts = roots(f_expr, x_sym)
            is_split_E = True
            if sum(rts.values()) != f_poly.degree():
                is_split_E = False
            else:
                for r in rts:
                    if not is_in_field(r, K_gens):
                        is_split_E = False
                        break
                if is_split_E:
                    E_and_roots = list(E_gens) + list(rts.keys())
                    for g in K_gens:
                        if not is_in_field(g, E_and_roots):
                            is_split_E = False
                            break
            neg_q = not is_split_E
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]