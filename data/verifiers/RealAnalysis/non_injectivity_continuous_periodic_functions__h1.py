import sympy
from sympy import Symbol, S, Eq, FiniteSet, diff, periodicity, MatrixBase, Union, Intersection, ImageSet, eye, zeros
from sympy.calculus.util import continuous_domain
from sympy.solvers.inequalities import reduce_inequalities

# Top-level setup
x = Symbol('x', real=True)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract expression if witness is a callable
    if callable(witness):
        try:
            f_expr = witness(x)
        except Exception:
            f_expr = witness
    else:
        f_expr = witness

    # H_1: f is continuous everywhere on R
    h1_ok = False
    try:
        if isinstance(f_expr, MatrixBase):
            is_cont = True
            for i in range(f_expr.rows):
                for j in range(f_expr.cols):
                    if continuous_domain(f_expr[i, j], x, S.Reals) != S.Reals:
                        is_cont = False
                        break
                if not is_cont:
                    break
            h1_ok = is_cont
        else:
            domain = continuous_domain(f_expr, x, S.Reals)
            h1_ok = (domain == S.Reals)
    except Exception:
        h1_ok = False

    # H_2: There exists a real number T > 0 such that f(x + T) = f(x) for all x in R
    h2_ok = False
    try:
        if isinstance(f_expr, MatrixBase):
            if all(e.is_constant() for e in f_expr):
                h2_ok = True
            else:
                all_periodic = True
                has_period = False
                for e in f_expr:
                    if e.is_constant() or len(e.free_symbols) == 0:
                        continue
                    p = periodicity(e, x)
                    if p is None or not p.is_real or p <= 0:
                        all_periodic = False
                        break
                    has_period = True
                h2_ok = all_periodic and has_period
        else:
            if hasattr(f_expr, 'is_constant') and f_expr.is_constant():
                h2_ok = True
            elif hasattr(f_expr, 'free_symbols') and len(f_expr.free_symbols) == 0:
                h2_ok = True
            else:
                p = periodicity(f_expr, x)
                if p is not None and p.is_real and p > 0:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The function f IS injective on R
    neg_q_ok = False
    try:
        y = Symbol('y', real=True)
        if isinstance(f_expr, MatrixBase):
            common_sol = S.Reals
            for i in range(f_expr.rows):
                for j in range(f_expr.cols):
                    eq = Eq(f_expr[i, j], f_expr[i, j].subs(x, y))
                    sol = sympy.solveset(eq, y, domain=S.Reals)
                    common_sol = Intersection(common_sol, sol)
            if common_sol == FiniteSet(x):
                neg_q_ok = True
        else:
            sol = sympy.solveset(Eq(f_expr, f_expr.subs(x, y)), y, domain=S.Reals)
            if sol == FiniteSet(x):
                neg_q_ok = True
            elif sol.is_FiniteSet and sol != FiniteSet(x):
                neg_q_ok = False
            elif isinstance(sol, (ImageSet, Union)):
                neg_q_ok = False
            elif sol == S.Reals:
                neg_q_ok = False
            else:
                # Fallback for scalar functions using monotonicity
                df = diff(f_expr, x)
                if df == 0:
                    neg_q_ok = False
                else:
                    try:
                        pos = reduce_inequalities(df >= 0, x)
                        if pos == S.Reals:
                            zeros_set = sympy.solveset(df, x, domain=S.Reals)
                            if isinstance(zeros_set, (FiniteSet, ImageSet, Union)) or zeros_set.is_FiniteSet:
                                neg_q_ok = True
                        else:
                            neg = reduce_inequalities(df <= 0, x)
                            if neg == S.Reals:
                                zeros_set = sympy.solveset(df, x, domain=S.Reals)
                                if isinstance(zeros_set, (FiniteSet, ImageSet, Union)) or zeros_set.is_FiniteSet:
                                    neg_q_ok = True
                    except Exception:
                        pass
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is continuous everywhere on R",
    "H_2: There exists a real number T > 0 such that f(x + T) = f(x) for all x in R",
    "¬Q: The function f is injective on R"
]

N_HYP = 2
NEG_Q_INDEX = 2