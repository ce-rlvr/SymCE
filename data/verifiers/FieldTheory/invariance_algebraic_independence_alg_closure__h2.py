import sympy
from sympy import QQ, ZZ, Symbol, Matrix
from sympy.polys.polyerrors import NotAlgebraic
from sympy.abc import x, y, z

# Top-level setup
# We define standard fields and symbols that might be used in the witness.
# The witness is expected to provide K, L, S, and K_bar.
# Since the hypothesis "K_bar is an algebraic closure of K" was dropped,
# K_bar can be any field, allowing S to be independent over K but dependent over K_bar.

def domain_contains(domain, expr):
    """Check if a SymPy domain contains a given expression."""
    try:
        expr_sym = sympy.sympify(expr)
        if hasattr(domain, 'from_sympy'):
            domain.from_sympy(expr_sym)
            return True
    except Exception:
        pass
    try:
        return expr in domain
    except Exception:
        return False

def is_algebraically_independent(S, K):
    """Check if a set of expressions S is algebraically independent over a field K."""
    if not S:
        return True
    
    S_list = list(S)
    
    # 1. If any element is in K, it is a root of X - s = 0, hence dependent.
    for s in S_list:
        if domain_contains(K, s):
            return False
            
    # 2. Check constant expressions for algebraic dependence over QQ
    for s in S_list:
        try:
            expr = sympy.sympify(s)
            if not expr.free_symbols:
                try:
                    sympy.minimal_polynomial(expr, Symbol('_dummy'))
                    return False
                except NotAlgebraic:
                    continue
                except Exception:
                    continue
        except Exception:
            pass
                
    # 3. Jacobian check for algebraic dependence of multiple expressions
    try:
        exprs = [sympy.sympify(s) for s in S_list]
        free_syms = set()
        for expr in exprs:
            free_syms.update(expr.free_symbols)
            
        k_syms = set()
        if hasattr(K, 'symbols'):
            k_syms = set(K.symbols)
            
        # Only differentiate with respect to symbols not in the base field K
        free_syms = list(free_syms - k_syms)
        
        if free_syms:
            J = Matrix([[sympy.diff(expr, sym) for sym in free_syms] for expr in exprs])
            if J.rank() < len(S_list):
                return False
    except Exception:
        pass
        
    return True

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        if isinstance(witness, dict):
            K = witness['K']
            L = witness['L']
            S = witness['S']
            K_bar = witness['K_bar']
        else:
            K, L, S, K_bar = witness
    except Exception:
        return [False, False, False]
        
    # H_1: L is a field extension of K
    try:
        h1 = getattr(L, 'is_Field', False) and hasattr(K, 'is_subset') and K.is_subset(L)
    except Exception:
        h1 = False
        
    # H_2: S is a subset of L
    try:
        h2 = all(domain_contains(L, s) for s in S)
    except Exception:
        h2 = False
        
    # ¬Q: S is algebraically independent over K if and only if S is algebraically independent over K_bar FAILS
    try:
        indep_K = is_algebraically_independent(S, K)
        indep_K_bar = is_algebraically_independent(S, K_bar)
        neg_q = (indep_K != indep_K_bar)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L is a field extension of K",
    "H_2: S is a subset of L",
    "¬Q: Algebraic independence of S over K is not equivalent to algebraic independence over K_bar"
]

N_HYP = 2
NEG_Q_INDEX = 2