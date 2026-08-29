import sympy
from sympy import limit, oo, Abs
from sympy.abc import x, y, z, n, k
import math

# Top-level setup
# Common symbols are imported from sympy.abc

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness should be a tuple of two sequences (a_n, b_n), which can be sympy 
    expressions, Python callables, or lists/tuples.
    """
    try:
        a_expr, b_expr = witness
    except Exception:
        return [False, False]
    
    # Determine the free variable if expressions are symbolic
    try:
        syms_a = a_expr.free_symbols if hasattr(a_expr, 'free_symbols') else set()
        syms_b = b_expr.free_symbols if hasattr(b_expr, 'free_symbols') else set()
        syms = syms_a.union(syms_b)
        if len(syms) == 1:
            n_var = list(syms)[0]
        else:
            n_var = sympy.Symbol('n')
            for s in syms:
                if s.name == 'n':
                    n_var = s
                    break
    except Exception:
        n_var = sympy.Symbol('n')

    def eval_seq(expr, idx):
        if isinstance(expr, (list, tuple)):
            if idx < len(expr):
                return complex(expr[idx])
            else:
                return 0.0
        elif hasattr(expr, 'subs'):
            val = expr.subs(n_var, idx).evalf()
            return complex(val)
        elif callable(expr):
            return complex(expr(idx))
        else:
            return complex(expr)

    # Hypothesis 1: There exists an integer N >= 0 such that |a_n| <= |b_n| for all n >= N
    h1_ok = False
    try:
        for N in range(100):
            all_le = True
            for idx in range(N, N + 100):
                try:
                    val_a = abs(eval_seq(a_expr, idx))
                    val_b = abs(eval_seq(b_expr, idx))
                    if val_a > val_b + 1e-9:
                        all_le = False
                        break
                except Exception:
                    all_le = False
                    break
            if all_le:
                h1_ok = True
                break
    except Exception:
        h1_ok = False

    # Conclusion: The radius of convergence R_a is greater than or equal to R_b
    # Negation: R_a < R_b
    neg_q_ok = False
    try:
        def get_R(expr):
            if hasattr(expr, 'is_zero') and expr.is_zero:
                return float('inf')
            if expr == 0:
                return float('inf')
            
            # Try symbolic limits first if it's a sympy expression
            if not callable(expr) and not isinstance(expr, (list, tuple)):
                try:
                    expr_next = expr.subs(n_var, n_var + 1)
                    L = limit(Abs(expr / expr_next), n_var, oo)
                    if L.is_number or L == oo:
                        return float(L) if L != oo else float('inf')
                except Exception:
                    pass
                try:
                    L2 = limit(Abs(expr)**(1/n_var), n_var, oo)
                    if L2 == 0:
                        return float('inf')
                    elif L2 == oo:
                        return 0.0
                    elif L2.is_number:
                        return 1.0 / float(L2)
                except Exception:
                    pass
            
            # Fallback to numerical limsup of the root test
            max_root = 0.0
            for idx in range(100, 150):
                try:
                    val = abs(eval_seq(expr, idx))
                    if val > 0:
                        try:
                            r = float(val) ** (1.0 / idx)
                        except OverflowError:
                            return 0.0
                        if r > max_root:
                            max_root = r
                except Exception:
                    pass
            if max_root == 0:
                return float('inf')
            return 1.0 / max_root

        R_a = get_R(a_expr)
        R_b = get_R(b_expr)
        
        if R_a < R_b - 1e-9:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exists an integer N >= 0 such that |a_n| <= |b_n| for all n >= N",
    "¬Q: The radius of convergence R_a is less than R_b"
]

N_HYP = 1
NEG_Q_INDEX = 1