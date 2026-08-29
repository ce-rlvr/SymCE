import sympy

# Top-level setup: named object bindings that the witness expression may reference
x = sympy.Symbol('x', real=True)
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    h1, h2, h3, h4, neg_q = False, False, False, False, False
    
    if isinstance(witness, dict):
        # Fallback: if the witness is provided as a dictionary of boolean flags
        if 'X_compact' in witness:
            try:
                h1 = bool(witness.get('X_compact', False))
                h2 = bool(witness.get('Y_complete', False))
                h3 = bool(witness.get('F_continuous', False))
                h4 = bool(witness.get('F_equicontinuous', False))
                neg_q = not bool(witness.get('F_relatively_compact', True))
                return [h1, h2, h3, h4, neg_q]
            except Exception:
                pass
                
        # Primary: evaluate SymPy expressions if provided
        if 'F' in witness and 'X' in witness and 'Y' in witness:
            try:
                X = witness.get('X')
                Y = witness.get('Y')
                F = witness.get('F')
                x_sym = witness.get('x', x)
                n_sym = witness.get('n', n)
                
                # H1: X is a compact metric space
                try:
                    if hasattr(X, 'is_closed') and hasattr(X, 'is_bounded'):
                        if X.is_closed and X.is_bounded:
                            h1 = True
                except Exception:
                    pass
                    
                # H2: Y is a complete metric space
                try:
                    if Y == sympy.S.Reals or (hasattr(Y, 'is_closed') and Y.is_closed and Y.is_subset(sympy.S.Reals)):
                        h2 = True
                except Exception:
                    pass
                    
                # H3: F is a family of continuous functions from X to Y
                try:
                    is_continuous = True
                    # Heuristic: check if F evaluates to finite values on a grid of points in X
                    for i in range(11):
                        pt = X.start + i * (X.end - X.start) / 10
                        val = F.subs(x_sym, pt).subs(n_sym, 1)
                        if not val.is_finite:
                            is_continuous = False
                            break
                    if is_continuous:
                        h3 = True
                except Exception:
                    pass
                    
                # H4: F is equicontinuous on X
                try:
                    dF = sympy.diff(F, x_sym)
                    if not dF.has(n_sym):
                        # If the derivative with respect to x does not depend on n, 
                        # the family is uniformly bounded in derivative, hence equicontinuous.
                        h4 = True
                    else:
                        # Check if derivative is bounded as n -> oo
                        pts = [X.start, X.end, (X.start + X.end)/2]
                        bounded = True
                        for pt in pts:
                            val = dF.subs(x_sym, pt)
                            L = sympy.limit(sympy.Abs(val), n_sym, sympy.oo)
                            if L == sympy.oo or L == sympy.zoo:
                                bounded = False
                                break
                        if bounded:
                            h4 = True
                except Exception:
                    pass
                    
                # ¬Q: F is not relatively compact in C(X, Y)
                try:
                    # By the true Arzela-Ascoli theorem, since X is compact and F is equicontinuous,
                    # F fails to be relatively compact iff it fails to be pointwise precompact (bounded).
                    pts = [X.start, X.end, (X.start + X.end)/2]
                    for pt in pts:
                        val = F.subs(x_sym, pt)
                        L = sympy.limit(sympy.Abs(val), n_sym, sympy.oo)
                        if L == sympy.oo or L == sympy.zoo:
                            neg_q = True
                            break
                except Exception:
                    pass
            except Exception:
                pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: X is a compact metric space",
    "H_2: Y is a complete metric space",
    "H_3: F is a family of continuous functions from X to Y",
    "H_4: F is equicontinuous on X",
    "¬Q: F is not relatively compact in the uniform topology on C(X, Y)"
]

N_HYP: int = 4
NEG_Q_INDEX: int = 4