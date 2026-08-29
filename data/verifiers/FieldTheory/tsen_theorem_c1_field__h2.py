import sympy
from sympy import Poly
import z3
from sympy.abc import x, y, z, w, u, v
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: K is an algebraically closed field
    try:
        K = witness.get('K')
        h1 = (K in ['C', 'AlgebraicallyClosedField', 'AlgebraicReals'])
    except Exception:
        h1 = False

    # H_2: f is a homogeneous polynomial of degree d in n variables over L
    try:
        f = witness.get('f')
        vars = witness.get('vars')
        L = witness.get('L')
        if f is not None and vars is not None and L is not None:
            poly = Poly(f, *vars)
            h2 = poly.is_homogeneous
            if h2:
                coeffs = poly.coeffs()
                if L == 'R':
                    h2 = all(c.is_real for c in coeffs)
                elif L == 'Q':
                    h2 = all(c.is_rational for c in coeffs)
                elif L == 'Z':
                    h2 = all(c.is_integer for c in coeffs)
                else:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: n > d
    try:
        f = witness.get('f')
        vars = witness.get('vars')
        if f is not None and vars is not None:
            poly = Poly(f, *vars)
            d = poly.homogeneous_order()
            if d is not None:
                n = len(vars)
                h3 = bool(n > d)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: f has no non-trivial zero in L
    try:
        f = witness.get('f')
        vars = witness.get('vars')
        L = witness.get('L')
        if f is not None and vars is not None and L is not None:
            if L == 'R':
                z3_vars = [z3.Real(str(v)) for v in vars]
            elif L in ['Q', 'Z']:
                z3_vars = [z3.Int(str(v)) for v in vars]
            else:
                return [h1, h2, h3, False]
            
            def to_z3(expr):
                if isinstance(expr, sympy.Symbol):
                    return z3_vars[vars.index(expr)]
                elif isinstance(expr, (sympy.Integer, int)):
                    return int(expr)
                elif isinstance(expr, sympy.Rational):
                    if L == 'R':
                        return z3.RealVal(int(expr.p)) / z3.RealVal(int(expr.q))
                    else:
                        raise ValueError("Rational not supported for Ints")
                elif isinstance(expr, sympy.Float):
                    if L == 'R':
                        return z3.RealVal(float(expr))
                    else:
                        raise ValueError("Float not supported for Ints")
                elif isinstance(expr, sympy.Add):
                    args = [to_z3(arg) for arg in expr.args]
                    res = args[0]
                    for arg in args[1:]:
                        res += arg
                    return res
                elif isinstance(expr, sympy.Mul):
                    args = [to_z3(arg) for arg in expr.args]
                    res = args[0]
                    for arg in args[1:]:
                        res *= arg
                    return res
                elif isinstance(expr, sympy.Pow):
                    base = to_z3(expr.base)
                    exp = int(expr.exp)
                    return base ** exp
                else:
                    if hasattr(expr, 'is_Integer') and expr.is_Integer:
                        return int(expr)
                    raise ValueError(f"Unsupported expr: {expr}")

            poly = Poly(f, *vars)
            if L in ['Q', 'Z']:
                # Clear denominators for Q to solve over Z
                lcm_val = 1
                for c in poly.coeffs():
                    if isinstance(c, sympy.Rational):
                        lcm_val = sympy.lcm(lcm_val, c.q)
                f_expr = sympy.expand(f * lcm_val)
            else:
                f_expr = sympy.expand(f)
                
            f_z3 = to_z3(f_expr)
            
            solver = z3.Solver()
            solver.add(f_z3 == 0)
            
            # Non-trivial zero means at least one variable is non-zero
            or_conds = [v != 0 for v in z3_vars]
            solver.add(z3.Or(*or_conds))
            
            res = solver.check()
            # If unsat, there are NO non-trivial zeros, so the conclusion FAILS (neg_Q is True)
            neg_q = (res == z3.unsat)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f is a homogeneous polynomial of degree d in n variables over L",
    "H_3: n > d",
    "¬Q: f has no non-trivial zero in L"
]

N_HYP = 3
NEG_Q_INDEX = 3