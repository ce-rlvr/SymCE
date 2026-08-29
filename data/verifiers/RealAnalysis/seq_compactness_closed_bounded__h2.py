import sympy
from sympy import S, Set, Interval, limit, oo, Abs, Symbol
import math

# Top-level setup
m = Symbol('m', integer=True, positive=True)
R = S.Reals
N = S.Naturals
Z = S.Integers

def get_norm(v):
    try:
        if isinstance(v, (tuple, list)):
            return sum(float(x)**2 for x in v)**0.5
        return abs(float(v))
    except Exception:
        return float(Abs(v))

def escapes_to_infinity(seq_func):
    try:
        vals = [get_norm(seq_func(i)) for i in range(1000, 1200)]
        min1 = min(vals[0:50])
        min2 = min(vals[50:100])
        min3 = min(vals[100:150])
        min4 = min(vals[150:200])
        if min1 < min2 < min3 < min4 and min4 > 10:
            return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        K = witness[0]
        x_m = witness[1]
        m_sym = None
        if len(witness) >= 3:
            m_sym = witness[2]
        elif hasattr(x_m, 'free_symbols'):
            symbols = list(x_m.free_symbols)
            if len(symbols) == 1:
                m_sym = symbols[0]
            elif len(symbols) > 1:
                for s in symbols:
                    if s.name == 'm':
                        m_sym = s
                        break
                if m_sym is None:
                    m_sym = symbols[0]
    except Exception:
        return [False, False, False]

    # H1: K is a closed subset of R^n
    try:
        h1 = False
        if isinstance(K, Set):
            if K == S.Reals:
                h1 = True
            elif getattr(K, 'is_closed', None) is True:
                h1 = True
            elif hasattr(K, 'boundary'):
                try:
                    if K.boundary.is_subset(K):
                        h1 = True
                except Exception:
                    pass
            
            if not h1 and isinstance(K, Interval):
                if not K.left_open and not K.right_open:
                    h1 = True
                elif not K.left_open and K.end == S.Infinity:
                    h1 = True
                elif not K.right_open and K.start == S.NegativeInfinity:
                    h1 = True
    except Exception:
        h1 = False

    # H2: (x_m) is a sequence such that x_m in K for all m
    try:
        h2 = True
        for i in range(1, 101):
            if callable(x_m):
                val = x_m(i)
            else:
                val = x_m.subs(m_sym, i)
            
            c = K.contains(val)
            if c == True:
                continue
            elif c == False:
                h2 = False
                break
            else:
                try:
                    if K.contains(float(val)) == False:
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: (x_m) does not have a convergent subsequence whose limit belongs to K
    try:
        neg_q = False
        if callable(x_m):
            neg_q = escapes_to_infinity(x_m)
        else:
            try:
                L = limit(Abs(x_m), m_sym, oo)
                if L == oo:
                    neg_q = True
            except Exception:
                pass
            
            if not neg_q:
                neg_q = escapes_to_infinity(lambda i: x_m.subs(m_sym, i))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a closed subset of R^n",
    "H_2: (x_m) is a sequence such that x_m in K for all m",
    "¬Q: (x_m) does not have a convergent subsequence whose limit belongs to K"
]

N_HYP = 2
NEG_Q_INDEX = 2