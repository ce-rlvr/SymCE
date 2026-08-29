import sympy
from sympy import Symbol, S

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def extract_witness(witness):
    """
    Extracts X, Y, f_n, x, n from the witness.
    Supports dictionary, tuple, or just the expression for f_n.
    """
    if isinstance(witness, dict):
        X = witness.get('X', sympy.S.Reals)
        Y = witness.get('Y', sympy.S.Reals)
        f_n = witness.get('f_n', witness.get('f', None))
        sym_x = witness.get('x', None)
        sym_n = witness.get('n', None)
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 5:
            X, Y, f_n, sym_x, sym_n = witness
        elif len(witness) == 3:
            X, Y = sympy.S.Reals, sympy.S.Reals
            f_n, sym_x, sym_n = witness
        else:
            X, Y = sympy.S.Reals, sympy.S.Reals
            f_n = witness
            sym_x, sym_n = None, None
    else:
        X, Y = sympy.S.Reals, sympy.S.Reals
        f_n = witness
        sym_x, sym_n = None, None

    # Guess symbols if not explicitly provided
    if sym_x is None or sym_n is None:
        if hasattr(f_n, 'free_symbols'):
            symbols = list(f_n.free_symbols)
            for s in symbols:
                if s.name == 'x':
                    sym_x = s
                elif s.name == 'n':
                    sym_n = s
            if sym_x is None and len(symbols) > 0:
                for s in symbols:
                    if s != sym_n:
                        sym_x = s
                        break
            if sym_n is None and len(symbols) > 0:
                for s in symbols:
                    if s != sym_x:
                        sym_n = s
                        break
                        
    if sym_x is None: sym_x = x
    if sym_n is None: sym_n = n
    
    return X, Y, f_n, sym_x, sym_n

def conditions(witness) -> list[bool]:
    X, Y, f_n, sym_x, sym_n = extract_witness(witness)
    
    # H_1: (X, d_X) and (Y, d_Y) are metric spaces
    try:
        h1 = X.is_subset(sympy.S.Reals) and Y.is_subset(sympy.S.Reals)
    except Exception:
        h1 = False
        
    # H_2: {f_n} is an equicontinuous sequence of functions from X to Y
    try:
        df = sympy.diff(f_n, sym_x)
        h2 = True
        test_points = [0, 0.5, 1, 2.5, 3.14159, -1, -2.5]
        if isinstance(X, sympy.Interval):
            start = X.start if X.start.is_finite else -10
            end = X.end if X.end.is_finite else 10
            test_points.extend([start, end, (start+end)/2])
            
        valid_points = []
        for pt in test_points:
            try:
                if X.contains(pt):
                    valid_points.append(pt)
            except Exception:
                pass
        if not valid_points:
            valid_points = [0]
            
        # Check if the derivative is bounded with respect to n
        for val_x in valid_points:
            for val_n in [1, 10, 100, 1000, 10000]:
                val = abs(df.subs({sym_x: val_x, sym_n: val_n}).evalf())
                if val > 100:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False
        
    # ¬Q: The limit function f is not continuous on X
    try:
        f = sympy.limit(f_n, sym_n, sympy.oo)
        
        if f.has(sympy.AccumBounds):
            neg_q = True
        elif isinstance(f, sympy.Limit):
            neg_q = True
        elif f in [sympy.oo, -sympy.oo, sympy.zoo]:
            neg_q = True
        else:
            from sympy.calculus.util import continuous_domain
            domain = continuous_domain(f, sym_x, X)
            if domain != X:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        # If limit or continuous_domain fails, the limit function likely doesn't exist or is ill-behaved
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: {f_n} is an equicontinuous sequence of functions from X to Y",
    "¬Q: The limit function f is not continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2