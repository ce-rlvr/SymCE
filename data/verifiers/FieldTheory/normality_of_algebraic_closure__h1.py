import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, CC, RR, QQ, Dummy, factor, degree, Poly, Mul, Pow

# Top-level setup
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
    "H_1: \\overline{K} is an algebraic closure of K",
    "¬Q: \\overline{K} is not a normal extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_algebraic_closure(K_bar, K):
    if isinstance(K_bar, str) and isinstance(K, str):
        L_str = K_bar.lower()
        K_str = K.lower()
        if L_str in ['c', 'cc', 'complex', 'complexes'] and K_str in ['r', 'rr', 'real', 'reals']:
            return True
        if L_str in ['q_bar', 'qbar', 'algebraic numbers'] and K_str in ['q', 'qq', 'rationals', 'rational']:
            return True
        base1 = L_str.replace('_bar', '')
        base2 = L_str.replace('bar', '')
        if base1 == K_str or base2 == K_str:
            return True
            
    if K_bar == CC and K == RR:
        return True
    return False

def is_normal_extension(L, K):
    if isinstance(L, str) and isinstance(K, str):
        L_str = L.lower()
        K_str = K.lower()
        if L_str in ['c', 'cc', 'complex', 'complexes'] and K_str in ['r', 'rr', 'real', 'reals']:
            return True
        if L_str in ['q_bar', 'qbar', 'algebraic numbers'] and K_str in ['q', 'qq', 'rationals', 'rational']:
            return True
        base1 = L_str.replace('_bar', '')
        base2 = L_str.replace('bar', '')
        if base1 == K_str or base2 == K_str:
            return True
            
    if L == CC and K == RR:
        return True
    if L == K:
        return True
        
    if hasattr(L, 'ext') and K == QQ:
        x = Dummy('x')
        ext = L.ext
        minpoly = ext.minpoly
        if hasattr(minpoly, 'as_expr'):
            p_expr = minpoly.as_expr(x)
        else:
            p_expr = minpoly(x)
        
        try:
            factored = factor(p_expr, extension=ext)
            if isinstance(factored, Mul):
                for arg in factored.args:
                    if arg.has(x):
                        if isinstance(arg, Pow):
                            base = arg.base
                        else:
                            base = arg
                        if degree(Poly(base, x)) > 1:
                            return False
                return True
            elif isinstance(factored, Pow):
                return degree(Poly(factored.base, x)) <= 1
            else:
                return degree(Poly(factored, x)) <= 1
        except Exception:
            pass
            
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K_bar, K = witness
        else:
            K_bar = witness
            if K_bar == CC:
                K = RR
            elif isinstance(K_bar, str) and K_bar.lower() in ['c', 'cc', 'complex']:
                K = "R"
            elif isinstance(K_bar, str) and K_bar.lower() in ['q_bar', 'qbar']:
                K = "Q"
            elif isinstance(K_bar, str) and (K_bar.lower().endswith('bar') or K_bar.lower().endswith('_bar')):
                K = K_bar.lower().replace('_bar', '').replace('bar', '')
            else:
                K = QQ
    except Exception:
        return [False, False]
        
    try:
        h1 = is_algebraic_closure(K_bar, K)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_normal_extension(K_bar, K)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]