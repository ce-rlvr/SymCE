import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import simplify

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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                m, a, b = witness
            elif len(witness) == 2:
                a, b = witness
                m = None
            elif len(witness) == 4:
                m, rank, a, b = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        h2 = isinstance(a, dict) and isinstance(b, dict)
        if m is not None and not (isinstance(m, (int, sympy.Integer)) and m >= 2):
            h2 = False
            
        def is_free_group_element(w):
            if isinstance(w, tuple):
                return all(isinstance(x, (int, sympy.Integer)) and x != 0 for x in w)
            if type(w).__name__ == 'FreeGroupElement':
                return True
            return False
            
        h1 = False
        if h2:
            h1 = True
            for w in list(a.keys()) + list(b.keys()):
                if not is_free_group_element(w):
                    h1 = False
                    break
                    
        neg_q = False
        if h1 and h2:
            def is_zero(c):
                if m is not None:
                    return c % m == 0
                else:
                    try:
                        return bool(simplify(c) == 0)
                    except Exception:
                        return c == 0
                        
            a_nonzero = any(not is_zero(c) for c in a.values())
            b_nonzero = any(not is_zero(c) for c in b.values())
            
            if a_nonzero and b_nonzero:
                prod = {}
                for w1, c1 in a.items():
                    for w2, c2 in b.items():
                        if isinstance(w1, tuple) and isinstance(w2, tuple):
                            w = []
                            for x in w1 + w2:
                                if w and isinstance(x, (int, sympy.Integer)) and isinstance(w[-1], (int, sympy.Integer)) and w[-1] == -x:
                                    w.pop()
                                else:
                                    w.append(x)
                            w = tuple(w)
                        else:
                            w = w1 * w2
                            
                        if m is not None:
                            prod[w] = (prod.get(w, 0) + c1 * c2) % m
                        else:
                            prod[w] = prod.get(w, 0) + c1 * c2
                            
                prod_zero = all(is_zero(c) for c in prod.values())
                neg_q = prod_zero
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: group ring of F over K is valid",
    "¬Q: group ring has non-zero zero divisors"
]

N_HYP = 2
NEG_Q_INDEX = 2