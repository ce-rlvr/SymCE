import sympy as sp
import math
import itertools
import functools
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: The sequence (x_n) is bounded.",
    "¬Q: The sequence (x_n) does NOT have a convergent subsequence."
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    'If a sequence is bounded, it has a convergent subsequence.'
    (This is false if the space is not complete, e.g., Q, or infinite-dimensional, e.g., C[0,1] or l^2).
    """
    h1_ok = False
    neg_q = False
    
    try:
        # Handle callable witness (e.g., lambda n, k: ...)
        if callable(witness):
            import inspect
            sig = inspect.signature(witness)
            if len(sig.parameters) == 2:
                h1_ok = True
                neg_q = True
                for i in range(1, 15):
                    norm_sq = sum(float(witness(i, j))**2 for j in range(1, 30))
                    if norm_sq > 100 or norm_sq < 0.01:
                        h1_ok = False
                for i in range(1, 10):
                    for j in range(i+1, 11):
                        dist_sq = sum(float(witness(i, k) - witness(j, k))**2 for k in range(1, 30))
                        if dist_sq < 0.1:
                            neg_q = False
                if h1_ok and neg_q:
                    return [True, True]
            elif len(sig.parameters) == 1:
                n_sym = sp.Symbol('n', integer=True, positive=True)
                expr = witness(n_sym)
            else:
                expr = witness()
        else:
            expr = witness
            
        # Handle SymPy Sequence objects
        if hasattr(expr, 'formula') and hasattr(expr, 'variables'):
            n_var = expr.variables[0]
            expr = expr.formula
        else:
            n_var = None

        # Handle Matrix sequences
        if isinstance(expr, sp.MatrixBase):
            free = list(expr.free_symbols)
            if len(free) == 1:
                n = free[0]
                try:
                    vals = [float(expr.subs(n, 10).norm()), float(expr.subs(n, 100).norm())]
                    if max(vals) < 1e6:
                        h1_ok = True
                except Exception:
                    pass
                try:
                    L_mat = [sp.limit(comp, n, sp.oo) for comp in expr]
                    if any(comp.is_real and comp.is_rational is False for comp in L_mat):
                        neg_q = True
                except Exception:
                    pass
            elif len(free) == 0:
                h1_ok = True
                neg_q = False

        # Handle standard SymPy expressions
        elif isinstance(expr, sp.Expr):
            free = list(expr.free_symbols)
            
            if len(free) == 2:
                # Sequence of functions or vectors
                n_cands = [s for s in free if s.name in ('n', 'k', 'm', 'i', 'j')]
                if len(n_cands) == 1:
                    n = n_cands[0]
                    x = [s for s in free if s != n][0]
                elif len(n_cands) >= 2:
                    n = n_cands[0]
                    x = n_cands[1]
                else:
                    n, x = free
                    
                # Check uniform boundedness on [0, 1]
                h1_ok = True
                try:
                    v10 = max([abs(float(expr.subs({n: 10, x: xv/10}))) for xv in range(0, 11)])
                    v100 = max([abs(float(expr.subs({n: 100, x: xv/10}))) for xv in range(0, 11)])
                    v1000 = max([abs(float(expr.subs({n: 1000, x: xv/10}))) for xv in range(0, 11)])
                    if v1000 > 100 and v1000 > v100 * 1.5 and v100 > v10 * 1.5:
                        h1_ok = False
                except Exception:
                    h1_ok = False
                    
                # Check equicontinuity (derivative bounded) for Arzela-Ascoli counterexamples
                try:
                    deriv = sp.diff(expr, x)
                    v10 = max([abs(float(deriv.subs({n: 10, x: xv/10}))) for xv in range(0, 11)])
                    v100 = max([abs(float(deriv.subs({n: 100, x: xv/10}))) for xv in range(0, 11)])
                    v1000 = max([abs(float(deriv.subs({n: 1000, x: xv/10}))) for xv in range(0, 11)])
                    if v1000 > 100 and v1000 > v100 * 1.5 and v100 > v10 * 1.5:
                        neg_q = True
                except Exception:
                    pass
                    
                # Check l2 boundedness and separation for l2 counterexamples
                if not neg_q:
                    try:
                        norm_10 = sum(float(expr.subs({n: 10, x: m}))**2 for m in range(1, 100))
                        norm_20 = sum(float(expr.subs({n: 20, x: m}))**2 for m in range(1, 100))
                        if norm_10 < 100 and norm_20 < 100:
                            dist_10_20 = sum(float(expr.subs({n: 10, x: m}) - expr.subs({n: 20, x: m}))**2 for m in range(1, 100))
                            dist_20_30 = sum(float(expr.subs({n: 20, x: m}) - expr.subs({n: 30, x: m}))**2 for m in range(1, 100))
                            if dist_10_20 > 0.5 and dist_20_30 > 0.5:
                                neg_q = True
                                h1_ok = True
                    except Exception:
                        pass
                        
            elif len(free) == 1 or n_var is not None:
                # Sequence of numbers
                n = n_var if n_var is not None else free[0]
                
                # Check boundedness
                try:
                    L_abs = sp.limit(sp.Abs(expr), n, sp.oo)
                    if L_abs == sp.oo or (hasattr(L_abs, 'max') and L_abs.max == sp.oo):
                        h1_ok = False
                    else:
                        h1_ok = True
                except Exception:
                    try:
                        v10 = abs(float(expr.subs(n, 10)))
                        v100 = abs(float(expr.subs(n, 100)))
                        v1000 = abs(float(expr.subs(n, 1000)))
                        if v1000 > 100 and v1000 > v100 * 1.5 and v100 > v10 * 1.5:
                            h1_ok = False
                        else:
                            h1_ok = True
                    except Exception:
                        h1_ok = False
                        
                # Check if it has no convergent subsequence in Q
                try:
                    L = sp.limit(expr, n, sp.oo)
                    if L.is_real and L.is_rational is False:
                        neg_q = True
                    elif L == sp.oo or L == -sp.oo:
                        neg_q = True
                    else:
                        L1 = sp.limit(expr.subs(n, 2*n), n, sp.oo)
                        L2 = sp.limit(expr.subs(n, 2*n+1), n, sp.oo)
                        if (L1.is_real and L1.is_rational is False) and \
                           (L2.is_real and L2.is_rational is False):
                            neg_q = True
                except Exception:
                    pass
                    
            elif len(free) == 0:
                h1_ok = True
                neg_q = False

        # Fallback for custom objects
        elif hasattr(witness, 'is_bounded') and hasattr(witness, 'has_convergent_subsequence'):
            try:
                h1_ok = bool(witness.is_bounded())
                neg_q = not bool(witness.has_convergent_subsequence())
            except Exception:
                pass

    except Exception:
        pass
        
    return [bool(h1_ok), bool(neg_q)]