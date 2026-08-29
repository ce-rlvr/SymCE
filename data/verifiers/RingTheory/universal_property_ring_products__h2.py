import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def get_attr(obj, attr, default=None):
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)

def make_callable(f):
    if isinstance(f, dict):
        return lambda x: f[x]
    return f

def is_ring(ring):
    try:
        elements = list(get_attr(ring, 'elements'))
        add = get_attr(ring, 'add')
        mul = get_attr(ring, 'mul')
        zero = get_attr(ring, 'zero')
        
        if add is None or mul is None or zero is None:
            return False
        if zero not in elements:
            return False
            
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a:
                return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv:
                return False
            for b in elements:
                if add(a, b) != add(b, a):
                    return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)):
                        return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)):
                        return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                        return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                        return False
                        
        one = get_attr(ring, 'one')
        if one is not None:
            if one not in elements:
                return False
            for a in elements:
                if mul(a, one) != a or mul(one, a) != a:
                    return False
        return True
    except Exception:
        return False

def is_homomorphism(f, R, S):
    try:
        elements = list(get_attr(R, 'elements'))
        add_R = get_attr(R, 'add')
        mul_R = get_attr(R, 'mul')
        add_S = get_attr(S, 'add')
        mul_S = get_attr(S, 'mul')
        
        for a in elements:
            for b in elements:
                if f(add_R(a, b)) != add_S(f(a), f(b)):
                    return False
                if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                    return False
                    
        one_R = get_attr(R, 'one')
        one_S = get_attr(S, 'one')
        if one_R is not None and one_S is not None:
            if f(one_R) != one_S:
                return False
                
        return True
    except Exception:
        return False

class DirectProductRing:
    def __init__(self, S1, S2):
        self.S1 = S1
        self.S2 = S2
        self.elements = [(x, y) for x in list(get_attr(S1, 'elements')) for y in list(get_attr(S2, 'elements'))]
        self.zero = (get_attr(S1, 'zero'), get_attr(S2, 'zero'))
        
        one1 = get_attr(S1, 'one')
        one2 = get_attr(S2, 'one')
        if one1 is not None and one2 is not None:
            self.one = (one1, one2)
        else:
            self.one = None
            
    def add(self, a, b):
        return (get_attr(self.S1, 'add')(a[0], b[0]), get_attr(self.S2, 'add')(a[1], b[1]))
        
    def mul(self, a, b):
        return (get_attr(self.S1, 'mul')(a[0], b[0]), get_attr(self.S2, 'mul')(a[1], b[1]))

def conditions(witness):
    try:
        R = get_attr(witness, 'R')
        S1 = get_attr(witness, 'S1')
        S2 = get_attr(witness, 'S2')
        
        h1 = is_ring(R) and is_ring(S1) and is_ring(S2)
    except Exception:
        h1 = False
        
    try:
        f1 = make_callable(get_attr(witness, 'f1'))
        f2 = make_callable(get_attr(witness, 'f2'))
        h2 = is_homomorphism(f1, R, S1) and is_homomorphism(f2, R, S2)
    except Exception:
        h2 = False
        
    try:
        pi1 = make_callable(get_attr(witness, 'pi1', lambda p: p[0]))
        pi2 = make_callable(get_attr(witness, 'pi2', lambda p: p[1]))
        
        P = DirectProductRing(S1, S2)
        
        elements_R = list(get_attr(R, 'elements'))
        elements_P = list(P.elements)
        
        valid_y = {}
        possible = True
        for i, x_val in enumerate(elements_R):
            valid_y[i] = []
            fx1 = f1(x_val)
            fx2 = f2(x_val)
            for y_val in elements_P:
                if pi1(y_val) == fx1 and pi2(y_val) == fx2:
                    valid_y[i].append(y_val)
            if not valid_y[i]:
                possible = False
                break
                
        if not possible:
            neg_q = True
        else:
            lists = [valid_y[i] for i in range(len(elements_R))]
            count = 0
            for combo in itertools.product(*lists):
                def f(x_val, combo=combo, elements_R=elements_R):
                    idx = elements_R.index(x_val)
                    return combo[idx]
                    
                if is_homomorphism(f, R, P):
                    count += 1
                    if count > 1:
                        break
            neg_q = (count != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R, S1, and S2 are rings",
    "H_2: f1: R -> S1 and f2: R -> S2 are ring homomorphisms",
    "¬Q: It is not the case that there exists a unique ring homomorphism f: R -> S1 x S2 such that pi1 o f = f1 and pi2 o f = f2"
]

N_HYP = 2
NEG_Q_INDEX = 2