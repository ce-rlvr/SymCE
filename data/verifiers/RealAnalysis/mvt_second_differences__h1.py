import sympy as sp
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
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
    "H_1: f is twice differentiable on (a - h, a + h)",
    "¬Q: There is no c in (a - h, a + h) such that f(a + h) - 2f(a) + f(a - h) = h^2 f''(c)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    witness is expected to be a tuple: (f_expr, a_val, h_val)
    where:
      - f_expr is a sympy expression (or string) representing f(x)
      - a_val is a real number
      - h_val is a positive real number
    """
    try:
        f_expr, a_val, h_val = witness
        if isinstance(f_expr, str):
            f_expr = sp.sympify(f_expr)
        else:
            f_expr = sp.sympify(f_expr)
        a_val = sp.sympify(a_val)
        h_val = sp.sympify(h_val)
        
        free_symbols = f_expr.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        else:
            var = x
    except Exception:
        return [False, False]

    # H_1: f is twice differentiable on (a - h, a + h)
    h1_ok = False
    try:
        if float(h_val) > 0:
            f2_expr = sp.diff(f_expr, var, 2)
            # Basic check: evaluate the second derivative at the midpoint
            val = f2_expr.subs(var, a_val)
            if val != sp.zoo and val != sp.nan and val.is_real is not False:
                h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: NO c in (a - h, a + h) such that f(a + h) - 2f(a) + f(a - h) = h^2 f''(c)
    neg_q_ok = False
    try:
        val_right = f_expr.subs(var, a_val + h_val)
        val_mid = f_expr.subs(var, a_val)
        val_left = f_expr.subs(var, a_val - h_val)
        
        target = val_right - 2*val_mid + val_left
        
        f2_expr = sp.diff(f_expr, var, 2)
        eq = h_val**2 * f2_expr - target
        
        # Find all real solutions to h^2 f''(x) - target = 0
        sols = sp.solveset(eq, var, domain=sp.S.Reals)
        
        if isinstance(sols, sp.ConditionSet):
            # Fallback if solveset cannot find exact solutions
            eq_simp = sp.simplify(eq)
            if eq_simp.is_constant():
                if float(eq_simp) != 0.0:
                    neg_q_ok = True
        else:
            # Intersect the solutions with the open interval (a - h, a + h)
            intersection = sp.Intersection(sols, sp.Interval.open(a_val - h_val, a_val + h_val))
            if intersection == sp.EmptySet:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]