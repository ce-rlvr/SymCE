import sympy
from sympy import S, ProductSet, Interval, simplify, diff, Matrix, Expr
import itertools

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    "H_1: U is an open, connected subset of R^n",
    "H_2: The gradient of f is the zero vector everywhere in U",
    "¬Q: f is not constant on U"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    U = None
    f = None
    vars = None
    
    try:
        if isinstance(witness, dict):
            U = witness.get('U')
            f = witness.get('f')
            vars = witness.get('vars')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                U, f = witness
            elif len(witness) == 3:
                vars, U, f = witness
        else:
            f = witness
            
        if f is None:
            return [False, False, False]
            
        from sympy import sympify
        f = sympify(f)
        
        if vars is None:
            if hasattr(f, 'free_symbols'):
                vars = tuple(sorted(f.free_symbols, key=lambda s: s.name))
            else:
                vars = ()
                
        if U is None:
            if len(vars) <= 1:
                U = S.Reals
            else:
                U = ProductSet(*[S.Reals for _ in vars])
                
        dim_U = 1
        if isinstance(U, ProductSet):
            dim_U = len(U.args)
        if len(vars) > 0 and dim_U != len(vars):
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H_1: U is an open, connected subset of R^n
    h1_ok = False
    try:
        def is_open_connected(s):
            if s == S.Reals:
                return True
            if isinstance(s, Interval):
                return s.left_open and s.right_open
            if isinstance(s, ProductSet):
                return all(is_open_connected(arg) for arg in s.args)
            try:
                if getattr(s, 'is_open', False) and getattr(s, 'is_connected', False):
                    return True
            except Exception:
                pass
            return False
            
        h1_ok = is_open_connected(U)
    except Exception:
        h1_ok = False

    # H_2: The gradient of f is the zero vector everywhere in U
    h2_ok = False
    try:
        if isinstance(f, (Matrix, list, tuple)):
            h2_ok = False
        elif not vars:
            h2_ok = True
        else:
            is_zero = True
            
            # Check continuity first to avoid piecewise false positives
            try:
                from sympy.calculus.util import continuous_domain
                for i, v in enumerate(vars):
                    dom = continuous_domain(f, v, S.Reals)
                    U_v = U
                    if isinstance(U, ProductSet):
                        U_v = U.args[i]
                        
                    if isinstance(U_v, Interval):
                        if not U_v.is_subset(dom):
                            is_zero = False
                            break
                    elif U_v == S.Reals:
                        if dom != S.Reals:
                            is_zero = False
                            break
            except Exception:
                pass
                
            if is_zero:
                for v in vars:
                    df = diff(f, v)
                    if simplify(df) != 0:
                        is_zero = False
                        break
            h2_ok = is_zero
    except Exception:
        h2_ok = False

    # ¬Q: f is not constant on U
    neg_q_ok = False
    try:
        def get_sample_points(u_set, n_points=3):
            if u_set == S.Reals:
                return [[0], [1], [-1]]
            if isinstance(u_set, Interval):
                a = float(u_set.start) if u_set.start != S.NegativeInfinity else -10.0
                b = float(u_set.end) if u_set.end != S.Infinity else 10.0
                if u_set.start == S.NegativeInfinity and u_set.end == S.Infinity:
                    return [[0], [1], [-1]]
                elif u_set.start == S.NegativeInfinity:
                    return [[b - 1], [b - 2], [b - 3]]
                elif u_set.end == S.Infinity:
                    return [[a + 1], [a + 2], [a + 3]]
                else:
                    d = (b - a) / (n_points + 1)
                    return [[a + i * d] for i in range(1, n_points + 1)]
            if isinstance(u_set, ProductSet):
                args_points = [get_sample_points(arg, n_points) for arg in u_set.args]
                prod = list(itertools.product(*args_points))
                return [ [x[0] for x in p] for p in prod ]
            return []

        if isinstance(f, (int, float)):
            neg_q_ok = False
        else:
            f_simp = simplify(f)
            if hasattr(f_simp, 'is_constant') and f_simp.is_constant():
                neg_q_ok = False
            elif hasattr(f_simp, 'free_symbols') and len(f_simp.free_symbols) == 0:
                neg_q_ok = False
            else:
                pts = get_sample_points(U)
                if pts and vars:
                    vals = []
                    for pt in pts:
                        subs_dict = dict(zip(vars, pt))
                        val = simplify(f.subs(subs_dict))
                        vals.append(val)
                    
                    is_const = True
                    for i in range(1, len(vals)):
                        diff_val = simplify(vals[i] - vals[0])
                        if diff_val != 0:
                            try:
                                if abs(float(diff_val.evalf())) > 1e-7:
                                    is_const = False
                                    break
                            except Exception:
                                is_const = False
                                break
                    neg_q_ok = not is_const
                else:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]