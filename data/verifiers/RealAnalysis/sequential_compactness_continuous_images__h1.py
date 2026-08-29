import sympy
from sympy.calculus.util import continuous_domain, function_range

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            K = witness['K']
            f = witness['f']
        else:
            K, f = witness
    except Exception:
        return [False, False]
        
    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
    except Exception:
        return [False, False]

    # H1: f is continuous on K
    try:
        dom = continuous_domain(f_expr, x, sympy.S.Reals)
        h1_ok = bool(K.is_subset(dom) and K.is_subset(sympy.S.Reals))
    except Exception:
        h1_ok = False

    # neg_Q: f(K) is NOT sequentially compact
    try:
        f_K = function_range(f_expr, x, K)
        
        def is_compact(S):
            if S == sympy.S.EmptySet:
                return True
            if isinstance(S, sympy.FiniteSet):
                return True
            if isinstance(S, sympy.Interval):
                if S.inf.is_finite == False or S.sup.is_finite == False:
                    return False
                if S.left_open or S.right_open:
                    return False
                return True
            if isinstance(S, sympy.Union):
                results = [is_compact(arg) for arg in S.args]
                if all(r is True for r in results):
                    return True
                if any(r is False for r in results):
                    return False
                return None
            if S == sympy.S.Reals:
                return False
            
            try:
                if S.is_subset(sympy.S.Reals) == False:
                    return False
                if S.inf.is_finite == False or S.sup.is_finite == False:
                    return False
            except Exception:
                pass
                
            return None
            
        comp = is_compact(f_K)
        if comp is False:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous function from K to R",
    "¬Q: The image f(K) is not sequentially compact"
]

N_HYP = 1
NEG_Q_INDEX = 1