import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            get = lambda k, d=None: witness.get(k, d)
            has = lambda k: k in witness
        else:
            get = lambda k, d=None: getattr(witness, k, d)
            has = lambda k: hasattr(witness, k)
            
        R = get('R')
        S = get('S')
        f_i = get('f_i')
        f = get('f')
        
        # H1: {S_i} is a family of rings
        h1 = isinstance(S, (list, tuple))
        
        # H2: f_i are ring homomorphisms
        h2 = isinstance(f_i, (list, tuple)) and len(f_i) == len(S)
        
        # H3: f is defined by f(x) = (f_i(x))
        h3 = True
        for x in R:
            fx = f(x) if callable(f) else f[x]
            expected = tuple((fi(x) if callable(fi) else fi[x]) for fi in f_i)
            
            if isinstance(fx, list):
                fx_tup = tuple(fx)
            elif isinstance(fx, tuple):
                fx_tup = fx
            else:
                try:
                    fx_tup = tuple(fx)
                except TypeError:
                    fx_tup = fx
                    
            if fx_tup != expected:
                if len(S) == 1 and fx == expected[0]:
                    pass
                else:
                    h3 = False
                    break
                    
        # Conclusion: ker(f) == intersection of ker(f_i)
        if has('zero_prod'):
            zero_prod = get('zero_prod')
        else:
            if not has('zero_R'):
                return [False, False, False, False]
            zero_R = get('zero_R')
            zero_prod = f(zero_R) if callable(f) else f[zero_R]
            
        ker_f = []
        for x in R:
            fx = f(x) if callable(f) else f[x]
            if fx == zero_prod:
                if x not in ker_f:
                    ker_f.append(x)
                    
        if len(S) == 0:
            if has('intersection'):
                intersection = get('intersection')
                if isinstance(intersection, set): 
                    intersection = list(intersection)
            else:
                intersection = "undefined"
        else:
            if has('zeros_S'):
                zeros_S = get('zeros_S')
            else:
                if not has('zero_R'):
                    return [False, False, False, False]
                zero_R = get('zero_R')
                zeros_S = [(fi(zero_R) if callable(fi) else fi[zero_R]) for fi in f_i]
                
            intersection = list(R)
            for i in range(len(S)):
                ker_fi = []
                for x in R:
                    fix = f_i[i](x) if callable(f_i[i]) else f_i[i][x]
                    if fix == zeros_S[i]:
                        if x not in ker_fi:
                            ker_fi.append(x)
                intersection = [x for x in intersection if x in ker_fi]
                
        if intersection == "undefined":
            neg_q = True
        else:
            neg_q = False
            if len(ker_f) != len(intersection):
                neg_q = True
            else:
                for x in ker_f:
                    if x not in intersection:
                        neg_q = True
                        break
                if not neg_q:
                    for x in intersection:
                        if x not in ker_f:
                            neg_q = True
                            break
                            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: {S_i} is a family of rings",
    "H_2: For each i, f_i is a ring homomorphism",
    "H_3: f is defined by f(x) = (f_i(x))",
    "¬Q: The kernel of f is not the intersection of ker(f_i)"
]

N_HYP = 3
NEG_Q_INDEX = 3