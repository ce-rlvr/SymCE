import sympy
from sympy import Symbol, Interval, Piecewise, limit, oo, S, solveset, imageset

# Top-level setup: named object bindings that the witness expression may reference
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: K is a subset of R^n",
    "H_2: K is compact",
    "¬Q: f(K) is not a compact subset of R^m"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_neg_Q(witness):
    K = witness.get('K')
    f = witness.get('f')
    sym_x = witness.get('x', x)
    
    if K is None or f is None:
        return False

    if callable(f):
        try:
            f = f(sym_x)
        except Exception:
            pass

    # 1. Check via limit point (unbounded or not closed)
    if 'limit_pt' in witness:
        p = witness['limit_pt']
        d = witness.get('dir', '+')
        
        if K.contains(p) == True:
            try:
                L = limit(f, sym_x, p, dir=d)
                if L == oo or L == -oo:
                    return True
                if L.is_real:
                    sols = solveset(f - L, sym_x, domain=K)
                    if sols == S.EmptySet:
                        return True
            except Exception:
                pass

    # 2. Check via sequence (unbounded or not closed)
    if 'seq' in witness:
        seq = witness['seq']
        sym_n = witness.get('n', n)
        
        in_K = True
        for val in [100, 1000, 10000]:
            if K.contains(seq.subs(sym_n, val)) != True:
                in_K = False
                break
                
        if in_K:
            f_seq = f.subs(sym_x, seq)
            try:
                L = limit(f_seq, sym_n, oo)
                if L == oo or L == -oo:
                    return True
                if L.is_real:
                    sols = solveset(f - L, sym_x, domain=K)
                    if sols == S.EmptySet:
                        return True
            except Exception:
                pass
            
            # Numeric fallback for unboundedness
            try:
                v1 = float(abs(f_seq.subs(sym_n, 100)))
                v2 = float(abs(f_seq.subs(sym_n, 1000)))
                v3 = float(abs(f_seq.subs(sym_n, 10000)))
                if v1 > 50 and v2 > 500 and v3 > 5000:
                    return True
            except Exception:
                pass

    # 3. Check via direct imageset evaluation
    try:
        img = imageset(sym_x, f, K)
        if img.is_bounded == False:
            return True
        if img.is_closed == False:
            return True
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    if not isinstance(witness, dict):
        return [False, False, False]

    try:
        K = witness['K']
        h1_ok = K.is_subset(S.Reals) == True
    except Exception:
        h1_ok = False

    try:
        K = witness['K']
        h2_ok = (K.is_closed == True) and (K.is_bounded == True)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = check_neg_Q(witness)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]